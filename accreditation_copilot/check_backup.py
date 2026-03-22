import sqlite3

conn = sqlite3.connect('accreditation_copilot/data/metadata_backup.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="institution"')
print(f'Institution chunks in backup: {cursor.fetchone()[0]}')

cursor.execute('SELECT COUNT(*) FROM chunks')
print(f'Total chunks in backup: {cursor.fetchone()[0]}')

conn.close()
