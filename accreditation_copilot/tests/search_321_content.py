import sqlite3

conn = sqlite3.connect('data/metadata.db')
cursor = conn.cursor()

# Search for chunks containing "3.2.1" in text
cursor.execute('''
    SELECT chunk_id, criterion, page, source, substr(text, 1, 200)
    FROM chunks 
    WHERE text LIKE '%3.2.1%' AND framework = 'NAAC'
    ORDER BY page
    LIMIT 10
''')
rows = cursor.fetchall()

print(f'Found {len(rows)} chunks containing "3.2.1" in text:\n')
for i, r in enumerate(rows, 1):
    print(f'{i}. Page {r[2]}, Criterion: {r[1]}')
    print(f'   Text: {r[4]}...')
    print()

# Also check chunks around page 63-65 (where 3.2.1 should be)
print('\n' + '='*80)
print('Chunks on pages 63-65 with criterion starting with "3.2":')
cursor.execute('''
    SELECT chunk_id, criterion, page, chunk_order, substr(text, 1, 150)
    FROM chunks 
    WHERE page BETWEEN 63 AND 65 
    AND framework = 'NAAC'
    AND (criterion LIKE '3.2%' OR text LIKE '%3.2.1%')
    ORDER BY page, chunk_order
''')
rows = cursor.fetchall()

for r in rows:
    print(f'\nPage {r[2]}, Order {r[3]}, Criterion: {r[1]}')
    print(f'  Text: {r[4]}...')

conn.close()
