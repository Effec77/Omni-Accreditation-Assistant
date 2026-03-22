import sqlite3

conn = sqlite3.connect('accreditation_copilot/data/metadata.db')
cursor = conn.cursor()

# Check source types
cursor.execute('SELECT DISTINCT source_type FROM chunks')
source_types = cursor.fetchall()
print("Source types in database:")
for st in source_types:
    if st[0]:
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type=?', (st[0],))
        count = cursor.fetchone()[0]
        print(f"  {st[0]}: {count} chunks")

# Check institution chunks specifically
cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="institution"')
inst_count = cursor.fetchone()[0]
print(f"\nTotal institution chunks: {inst_count}")

if inst_count == 0:
    print("\n⚠️ WARNING: No institution chunks found!")
    print("This explains why all audits are getting 0 scores.")
    print("\nYou need to upload institutional documents first.")

conn.close()
