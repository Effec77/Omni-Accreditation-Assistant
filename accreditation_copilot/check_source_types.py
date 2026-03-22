import sqlite3

conn = sqlite3.connect('data/metadata.db')
cursor = conn.cursor()

cursor.execute('SELECT DISTINCT source_type FROM chunks')
source_types = cursor.fetchall()

print("Source types in data/metadata.db:")
for st in source_types:
    cursor.execute(f'SELECT COUNT(*) FROM chunks WHERE source_type=?', (st[0],))
    count = cursor.fetchone()[0]
    print(f"  {st[0]}: {count} chunks")

# Check if there's a framework column
cursor.execute('PRAGMA table_info(chunks)')
columns = cursor.fetchall()
print("\nColumns in chunks table:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check framework distribution
cursor.execute('SELECT DISTINCT framework FROM chunks')
frameworks = cursor.fetchall()
print("\nFrameworks:")
for fw in frameworks:
    cursor.execute(f'SELECT COUNT(*) FROM chunks WHERE framework=?', (fw[0],))
    count = cursor.fetchone()[0]
    print(f"  {fw[0]}: {count} chunks")

conn.close()
