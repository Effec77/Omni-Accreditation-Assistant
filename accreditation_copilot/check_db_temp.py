import sqlite3
from pathlib import Path

db_path = Path("data/metadata.db")
print(f"Database path: {db_path.absolute()}")
print(f"Exists: {db_path.exists()}")

if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    conn.close()
