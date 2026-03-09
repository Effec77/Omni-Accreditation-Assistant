import sqlite3
from pathlib import Path

db_path = Path("data/metadata.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get Excellence University chunks
cursor.execute("""
    SELECT chunk_id, text, source 
    FROM chunks 
    WHERE source LIKE '%Excellence%' 
    LIMIT 10
""")

print("\n" + "="*80)
print("EXCELLENCE UNIVERSITY CHUNK CONTENT")
print("="*80)

for chunk_id, text, source in cursor.fetchall():
    print(f"\nChunk ID: {chunk_id}")
    print(f"Source: {source}")
    print(f"Text: {text[:200]}...")
    print(f"Contains 'INR': {'INR' in text or 'inr' in text.lower()}")
    print(f"Contains 'Lakhs': {'Lakhs' in text or 'lakhs' in text.lower()}")
    print(f"Contains 'DST': {'DST' in text or 'dst' in text.lower()}")
    print(f"Contains 'projects': {'projects' in text.lower()}")

conn.close()
