"""
Cross-Boundary Validation Check
Ensures no chunk crosses criterion boundaries.
"""

import sqlite3
import re


def normalize_to_metric_level(raw_id: str) -> str:
    """Normalize criterion ID to metric level."""
    parts = raw_id.split(".")
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return raw_id


def check_cross_boundary_chunks(db_path: str = "data/metadata.db") -> bool:
    """
    Check for chunks that cross criterion boundaries.
    
    A chunk crosses boundaries if it contains headers for multiple criteria.
    
    Returns:
        True if no violations found, False otherwise
    """
    print("\n" + "="*60)
    print("CROSS-BOUNDARY VALIDATION CHECK")
    print("="*60)
    
    conn = sqlite3.connect(db_path)
    
    cursor = conn.execute("""
        SELECT chunk_id, criterion, text
        FROM chunks
        WHERE framework='NAAC'
        AND criterion IS NOT NULL
    """)
    
    violations = []
    
    for chunk_id, criterion, text in cursor.fetchall():
        # Find all "Weightage X.Y.Z QnM" headers in chunk
        headers = re.findall(
            r'Weightage\s+([1-7]\.\d{1,2}\.\d{1,2})\s+QnM', text
        )
        
        # Normalize all found headers
        normalized_headers = [normalize_to_metric_level(h) for h in headers]
        
        # Check if any header differs from chunk's criterion
        for h in normalized_headers:
            if h != criterion:
                violations.append({
                    'chunk_id': chunk_id,
                    'labeled_as': criterion,
                    'contains': h,
                    'text_preview': text[:200]
                })
    
    conn.close()
    
    if violations:
        print(f"\n❌ FAIL: Found {len(violations)} cross-boundary violations\n")
        for v in violations[:5]:  # Show first 5
            print(f"Chunk: {v['chunk_id']}")
            print(f"  Labeled as: {v['labeled_as']}")
            print(f"  Contains header: {v['contains']}")
            print(f"  Preview: {v['text_preview']}...")
            print()
        return False
    else:
        print("\n✅ PASS: Zero cross-boundary chunks")
        print("All chunks respect criterion boundaries.")
        return True


if __name__ == "__main__":
    result = check_cross_boundary_chunks()
    exit(0 if result else 1)
