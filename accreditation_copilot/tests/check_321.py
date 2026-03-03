import sqlite3

conn = sqlite3.connect('data/metadata.db')
cursor = conn.cursor()

# Check for 3.2.1 chunks
cursor.execute('SELECT chunk_id, criterion, page, substr(text, 1, 100) FROM chunks WHERE criterion = "3.2.1"')
rows = cursor.fetchall()

print(f'Found {len(rows)} chunks with criterion 3.2.1:')
for r in rows:
    print(f'  {r[0]}, criterion={r[1]}, page={r[2]}')
    print(f'  Text: {r[3]}...\n')

conn.close()
