import sqlite3
from pathlib import Path

db_path = Path("data/metadata.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check what's in the database
cursor.execute("SELECT DISTINCT source, COUNT(*) FROM chunks WHERE source_type='institution' GROUP BY source")
results = cursor.fetchall()

print("\n=== Institution Chunks in Database ===")
for source, count in results:
    print(f"{source}: {count} chunks")

# Check if Excellence University is there
cursor.execute("SELECT COUNT(*) FROM chunks WHERE source LIKE '%Excellence%'")
excellence_count = cursor.fetchone()[0]
print(f"\nExcellence University chunks: {excellence_count}")

conn.close()
