from ingestion.institution.pdf_parser import PDFParser
from pathlib import Path

parser = PDFParser()

pdfs = [
    "Riverton_Bplus_SSR.pdf",
    "Excellence_University_A+_SSR.pdf"
]

for pdf_name in pdfs:
    pdf_path = Path("data/raw_docs") / pdf_name
    doc = parser.parse(str(pdf_path))
    total_text = sum(len(p.get("text", "")) for p in doc["pages"])
    print(f"\n{pdf_name}:")
    print(f"  Pages: {len(doc['pages'])}")
    print(f"  Total text length: {total_text} characters")
    print(f"  Tables: {sum(len(p.get('tables', [])) for p in doc['pages'])}")
