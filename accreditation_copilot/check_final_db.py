import sqlite3

conn = sqlite3.connect('accreditation_copilot/data/metadata.db')
cursor = conn.cursor()

cursor.execute('SELECT DISTINCT source_type FROM chunks')
source_types = cursor.fetchall()

print("Source types in accreditation_copilot/data/metadata.db:")
for st in source_types:
    if st[0]:  # Not NULL
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type=?', (st[0],))
        count = cursor.fetchone()[0]
        print(f"  {st[0]}: {count} chunks")

# Check NULL source_type
cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type IS NULL')
null_count = cursor.fetchone()[0]
if null_count > 0:
    print(f"  NULL: {null_count} chunks")

# Check frameworks
cursor.execute('SELECT DISTINCT framework FROM chunks')
frameworks = cursor.fetchall()
print("\nFrameworks:")
for fw in frameworks:
    if fw[0]:
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE framework=?', (fw[0],))
        count = cursor.fetchone()[0]
        print(f"  {fw[0]}: {count} chunks")

conn.close()
