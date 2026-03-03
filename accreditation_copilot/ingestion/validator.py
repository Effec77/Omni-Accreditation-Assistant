"""
Ingestion Integrity Validator
Validates ingestion quality before indices are built.
"""

import sqlite3
import re
import sys


def validate_ingestion_integrity(db_path: str) -> bool:
    """
    Ingestion integrity gate. Must pass before indices are built.
    Returns True if clean, False if issues found.
    Prints detailed report either way.
    """
    conn = sqlite3.connect(db_path)
    issues = []
    warnings = []
    
    print("\n" + "="*60)
    print("INGESTION INTEGRITY VALIDATION")
    print("="*60)
    
    # Check 1 — No malformed NAAC criterion labels
    cursor = conn.execute("""
        SELECT criterion, COUNT(*) as count
        FROM chunks
        WHERE framework = 'NAAC'
        AND criterion IS NOT NULL
        GROUP BY criterion
    """)
    for criterion, count in cursor.fetchall():
        if not re.fullmatch(r'[1-7]\.\d{1,2}(\.\d{1,2})?', criterion):
            issues.append(f"MALFORMED criterion label: '{criterion}' ({count} chunks)")
    
    # Check 2 — No four-level submetric IDs stored as labels
    cursor = conn.execute("""
        SELECT criterion, COUNT(*)
        FROM chunks
        WHERE criterion LIKE '%.%.%.%'
        AND criterion IS NOT NULL
    """)
    submetrics = cursor.fetchall()
    for criterion, count in submetrics:
        if criterion:  # Skip None values
            issues.append(f"SUBMETRIC stored as label: '{criterion}' ({count} chunks)")
    
    # Check 3 — Label present in chunk text
    cursor = conn.execute("""
        SELECT chunk_id, criterion, text
        FROM chunks
        WHERE criterion IS NOT NULL
        AND framework = 'NAAC'
        LIMIT 200
    """)
    mismatch_count = 0
    for chunk_id, criterion, text in cursor.fetchall():
        if criterion and criterion not in text:
            mismatch_count += 1
    if mismatch_count > 0:
        warnings.append(
            f"LABEL NOT IN TEXT: {mismatch_count} chunks where "
            f"criterion label does not appear in chunk text"
        )
    
    # Check 4 — Suspicious single-chunk criteria
    cursor = conn.execute("""
        SELECT criterion, COUNT(*) as count
        FROM chunks
        WHERE framework = 'NAAC'
        AND criterion IS NOT NULL
        GROUP BY criterion
        HAVING count = 1
        ORDER BY criterion
    """)
    singles = cursor.fetchall()
    if len(singles) > 20:
        warnings.append(
            f"HIGH SINGLE-CHUNK COUNT: {len(singles)} criteria "
            f"with only 1 chunk — possible mislabeling"
        )
    
    # Check 5 — Framework coverage
    cursor = conn.execute(
        "SELECT framework, COUNT(*) FROM chunks GROUP BY framework"
    )
    print("\nFramework Coverage:")
    for framework, count in cursor.fetchall():
        print(f"  {framework}: {count} chunks")
    
    # Report
    print()
    if issues:
        print(f"CRITICAL ISSUES ({len(issues)}) - INGESTION FAILED:")
        for issue in issues:
            print(f"  [X] {issue}")
        print("\nFix these before building indices.")
        conn.close()
        return False
    
    if warnings:
        print(f"WARNINGS ({len(warnings)}) - Review before proceeding:")
        for w in warnings:
            print(f"  [!] {w}")
    
    if not issues and not warnings:
        print("  [OK] All integrity checks passed")
    elif not issues:
        print("  [OK] No critical issues - warnings noted above")
    
    conn.close()
    return True
