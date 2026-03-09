import sqlite3
from pathlib import Path

db_path = Path("data/metadata.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Delete old Excellence University chunks
cursor.execute("DELETE FROM chunks WHERE source LIKE '%Excellence%'")
deleted = cursor.rowcount
conn.commit()
conn.close()

print(f"Deleted {deleted} old Excellence University chunks")
print("Now re-ingest the new PDF!")
