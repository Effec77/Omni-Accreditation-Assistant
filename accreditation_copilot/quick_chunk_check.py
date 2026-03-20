import sqlite3
conn = sqlite3.connect("data/metadata.db")
cursor = conn.execute("SELECT source, COUNT(*) FROM chunks WHERE source_type='institution' GROUP BY source")
for row in cursor:
    print(f"{row[0]}: {row[1]} chunks")
conn.close()
