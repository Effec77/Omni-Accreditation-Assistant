from pathlib import Path
from ingestion.institution.run_institution_ingestion import run_institution_ingestion

# Temporarily move other PDFs
raw_docs = Path("data/raw_docs")
temp_dir = Path("data/temp_pdfs")
temp_dir.mkdir(exist_ok=True)

# Move all PDFs except Excellence to temp
for pdf in raw_docs.glob("*.pdf"):
    if "Excellence" not in pdf.name:
        pdf.rename(temp_dir / pdf.name)
        print(f"Moved {pdf.name} to temp")

# Ingest only Excellence
print("\n" + "="*60)
print("Ingesting Excellence University PDF only...")
print("="*60)
result = run_institution_ingestion("data/raw_docs")
print(f"\nResult: {result}")

# Move PDFs back
for pdf in temp_dir.glob("*.pdf"):
    pdf.rename(raw_docs / pdf.name)
    print(f"Moved {pdf.name} back")

temp_dir.rmdir()
