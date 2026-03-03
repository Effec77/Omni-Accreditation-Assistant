import sqlite3

conn = sqlite3.connect('data/metadata.db')
cursor = conn.cursor()

# Check for 3.2.1 chunks with full details
cursor.execute('''
    SELECT chunk_id, criterion, page, source, framework, doc_type, text 
    FROM chunks 
    WHERE criterion = "3.2.1"
''')
rows = cursor.fetchall()

print(f'Found {len(rows)} chunks with criterion 3.2.1:\n')
for r in rows:
    print(f'Chunk ID: {r[0]}')
    print(f'Criterion: {r[1]}')
    print(f'Page: {r[2]}')
    print(f'Source: {r[3]}')
    print(f'Framework: {r[4]}')
    print(f'Doc Type: {r[5]}')
    print(f'\nFull Text:')
    print(r[6])
    print('\n' + '='*80 + '\n')

# Also check what's on page 63
print('\nAll chunks on page 63:')
cursor.execute('''
    SELECT chunk_id, criterion, chunk_order, substr(text, 1, 150)
    FROM chunks 
    WHERE page = 63 AND source LIKE '%NAAC%'
    ORDER BY chunk_order
''')
rows = cursor.fetchall()

for r in rows:
    print(f'\nChunk {r[2]}: criterion={r[1]}')
    print(f'  Text: {r[3]}...')

conn.close()
