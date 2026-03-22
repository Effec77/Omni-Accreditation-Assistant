import sqlite3
from pathlib import Path

# Check all possible database locations
db_paths = [
    'accreditation_copilot/data/metadata.db',
    'data/metadata.db',
    'accreditation_copilot/indexes/metadata.db',
]

for db_path in db_paths:
    if Path(db_path).exists():
        print(f"\n{db_path}:")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="framework"')
        framework_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM chunks')
        total_count = cursor.fetchone()[0]
        
        print(f"  Framework chunks: {framework_count}")
        print(f"  Total chunks: {total_count}")
        
        conn.close()
    else:
        print(f"\n{db_path}: NOT FOUND")
