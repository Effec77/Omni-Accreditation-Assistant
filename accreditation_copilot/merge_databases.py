"""
Merge framework chunks from data/metadata.db into accreditation_copilot/data/metadata.db
"""
import sqlite3
import shutil
from pathlib import Path

# Backup first
backup_path = "accreditation_copilot/data/metadata_backup.db"
if Path("accreditation_copilot/data/metadata.db").exists():
    shutil.copy("accreditation_copilot/data/metadata.db", backup_path)
    print(f"✓ Backup created: {backup_path}")

# Restore from backup (since we just overwrote it)
if Path(backup_path).exists():
    shutil.copy(backup_path, "accreditation_copilot/data/metadata.db")
    print("✓ Restored institution database from backup")

# Now merge framework chunks
source_db = "data/metadata.db"  # Has framework chunks
target_db = "accreditation_copilot/data/metadata.db"  # Has institution chunks

print(f"\nMerging databases:")
print(f"  Source (framework): {source_db}")
print(f"  Target (institution): {target_db}")

# Connect to both databases
source_conn = sqlite3.connect(source_db)
target_conn = sqlite3.connect(target_db)

source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

# Get framework chunks from source
source_cursor.execute('SELECT * FROM chunks WHERE source_type="framework"')
framework_chunks = source_cursor.fetchall()

print(f"\n✓ Found {len(framework_chunks)} framework chunks to merge")

# Get column names
source_cursor.execute('PRAGMA table_info(chunks)')
columns = [col[1] for col in source_cursor.fetchall()]

# Insert framework chunks into target
placeholders = ','.join(['?' for _ in columns])
insert_sql = f'INSERT OR REPLACE INTO chunks ({",".join(columns)}) VALUES ({placeholders})'

for chunk in framework_chunks:
    target_cursor.execute(insert_sql, chunk)

target_conn.commit()

# Verify
target_cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="framework"')
framework_count = target_cursor.fetchone()[0]

target_cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="institution"')
institution_count = target_cursor.fetchone()[0]

target_cursor.execute('SELECT COUNT(*) FROM chunks')
total_count = target_cursor.fetchone()[0]

print(f"\n✓ Merge complete!")
print(f"\nFinal counts in {target_db}:")
print(f"  Framework chunks: {framework_count}")
print(f"  Institution chunks: {institution_count}")
print(f"  Total chunks: {total_count}")

source_conn.close()
target_conn.close()

print("\n✓ SUCCESS: Framework and institution chunks are now in the same database!")
print(f"  Location: {target_db}")
