"""
Test framework coverage - check what criteria have framework data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import sqlite3

# Check framework chunks in metadata.db
db_path = "accreditation_copilot/data/metadata.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("FRAMEWORK CHUNKS ANALYSIS")
print("="*80)

# Get all framework chunks
cursor.execute("""
    SELECT chunk_id, source_file, child_text 
    FROM chunks 
    WHERE source_type = 'framework'
    ORDER BY source_file
""")

chunks = cursor.fetchall()
print(f"\nTotal framework chunks: {len(chunks)}")

# Group by source file
from collections import defaultdict
by_file = defaultdict(list)
for chunk_id, source_file, text in chunks:
    by_file[source_file].append((chunk_id, text[:100]))

print("\nFramework chunks by source file:")
for file, file_chunks in by_file.items():
    print(f"\n{file}: {len(file_chunks)} chunks")
    # Check if any criteria are mentioned
    criteria_mentioned = set()
    for chunk_id, text in file_chunks:
        # Look for criterion patterns
        import re
        matches = re.findall(r'\b\d+\.\d+\.\d+\b', text)
        criteria_mentioned.update(matches)
    
    if criteria_mentioned:
        print(f"  Criteria mentioned: {sorted(criteria_mentioned)}")
    else:
        print(f"  No specific criteria IDs found in text")

conn.close()

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("If you see only 3.2.1 or limited criteria above, that's why other")
print("criteria don't work - the framework index doesn't have data for them.")
print("\nSOLUTION: Add NAAC manual PDFs that describe ALL 11 criteria to:")
print("  accreditation_copilot/data/raw_docs/naac/")
