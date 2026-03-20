"""
NUCLEAR CACHE CLEAR - Clears EVERYTHING
"""
import sqlite3
import shutil
from pathlib import Path

print("\n" + "="*80)
print("NUCLEAR CACHE CLEAR - CLEARING EVERYTHING")
print("="*80)

# 1. Clear database
db_path = Path("data/metadata.db")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.execute("DELETE FROM chunks WHERE source_type='institution'")
    conn.commit()
    conn.execute("VACUUM")
    conn.commit()
    conn.close()
    print("✅ Database cleared and vacuumed")

# 2. Clear indexes
indexes_dir = Path("indexes/institution")
if indexes_dir.exists():
    shutil.rmtree(indexes_dir)
    indexes_dir.mkdir(parents=True)
    print("✅ Indexes directory cleared")

# 3. Clear audit cache
audit_cache_dir = Path("audit_results")
if audit_cache_dir.exists():
    for file in audit_cache_dir.glob("cache_*.json"):
        file.unlink()
    print("✅ Audit cache cleared")

# 4. Clear raw_docs
raw_docs = Path("data/raw_docs")
if raw_docs.exists():
    for pdf in raw_docs.glob("*.pdf"):
        pdf.unlink()
    print("✅ Raw docs cleared")

print("\n" + "="*80)
print("NUCLEAR CLEAR COMPLETE - System is 100% clean")
print("="*80)
print("\nNow upload a fresh PDF and ingest it.")
