import sqlite3

conn = sqlite3.connect('accreditation_copilot/data/metadata.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="framework"')
framework_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="institution"')
institution_count = cursor.fetchone()[0]

print(f'Framework chunks: {framework_count}')
print(f'Institution chunks: {institution_count}')

if framework_count > 0:
    cursor.execute('SELECT DISTINCT source FROM chunks WHERE source_type="framework"')
    files = cursor.fetchall()
    print(f'\nFramework files:')
    for f in files:
        print(f'  - {f[0]}')

conn.close()
