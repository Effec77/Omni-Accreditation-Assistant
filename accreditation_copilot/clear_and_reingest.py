import sqlite3
from pathlib import Path
from ingestion.institution.run_institution_ingestion import run_institution_ingestion

# Clear all institution data
db_path = Path("data/metadata.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("DELETE FROM chunks WHERE source_type='institution'")
deleted = cursor.rowcount
conn.commit()
conn.close()

print(f"\n{'='*70}")
print(f"Cleared {deleted} old institution chunks")
print(f"{'='*70}\n")

# Move old PDFs to temp
raw_docs = Path("data/raw_docs")
temp_dir = Path("data/temp_old_pdfs")
temp_dir.mkdir(exist_ok=True)

old_pdfs = ["Greenfield_MissingEvidence_SSR.pdf", "NorthValley_Almost_Aplus_SSR.pdf", "Riverton_Bplus_SSR.pdf"]
for pdf_name in old_pdfs:
    pdf_path = raw_docs / pdf_name
    if pdf_path.exists():
        pdf_path.rename(temp_dir / pdf_name)
        print(f"Moved {pdf_name} to temp")

# Ingest only new PDFs
print(f"\n{'='*70}")
print("Ingesting NEW table-heavy PDFs...")
print(f"{'='*70}\n")

result = run_institution_ingestion("data/raw_docs")
print(f"\nResult: {result}")

# Move old PDFs back
for pdf_name in old_pdfs:
    temp_path = temp_dir / pdf_name
    if temp_path.exists():
        temp_path.rename(raw_docs / pdf_name)
        print(f"Moved {pdf_name} back")

if temp_dir.exists():
    temp_dir.rmdir()

print(f"\n{'='*70}")
print("READY TO TEST!")
print(f"{'='*70}")
print("\nNow test in the UI:")
print("1. Excellence_University_A+_SSR.pdf - Should get A+ grade (85-95% confidence)")
print("2. Struggling_College_C_SSR.pdf - Should get C grade (5-15% confidence)")
