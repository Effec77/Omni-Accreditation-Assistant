"""
Compare chunk generation between two PDFs
"""
import sqlite3
from pathlib import Path
import json

def analyze_current_chunks():
    """Show current chunks in database"""
    db_path = Path("data/metadata.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(str(db_path))
    
    # Get chunk count by source
    cursor = conn.execute("""
        SELECT source, COUNT(*) as count, 
               MIN(LENGTH(text)) as min_len,
               MAX(LENGTH(text)) as max_len,
               AVG(LENGTH(text)) as avg_len
        FROM chunks 
        WHERE source_type='institution'
        GROUP BY source
    """)
    
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("CURRENT CHUNKS IN DATABASE")
    print("="*80)
    
    if not results:
        print("✅ No institution chunks found (database is clean)")
        conn.close()
        return
    
    for source, count, min_len, max_len, avg_len in results:
        print(f"\n📄 Source: {source}")
        print(f"   Chunks: {count}")
        print(f"   Text Length: min={min_len}, max={max_len}, avg={avg_len:.0f}")
    
    # Show sample chunks
    print("\n" + "="*80)
    print("SAMPLE CHUNKS (first 3)")
    print("="*80)
    
    cursor = conn.execute("""
        SELECT chunk_id, source, page, LENGTH(text) as text_len, 
               SUBSTR(text, 1, 100) as text_preview
        FROM chunks 
        WHERE source_type='institution'
        ORDER BY chunk_id
        LIMIT 3
    """)
    
    for chunk_id, source, page, text_len, text_preview in cursor:
        print(f"\nChunk {chunk_id}:")
        print(f"  Source: {source}")
        print(f"  Page: {page}")
        print(f"  Length: {text_len} chars")
        print(f"  Preview: {text_preview.replace(chr(10), ' ')}...")
    
    conn.close()

def check_raw_pdfs():
    """Check what PDFs are in raw_docs"""
    raw_docs = Path("data/raw_docs")
    
    print("\n" + "="*80)
    print("PDFs IN RAW_DOCS DIRECTORY")
    print("="*80)
    
    if not raw_docs.exists():
        print("❌ raw_docs directory not found")
        return
    
    pdfs = list(raw_docs.glob("*.pdf"))
    
    if not pdfs:
        print("✅ No PDFs (ready for fresh upload)")
        return
    
    print(f"\nFound {len(pdfs)} PDF(s):")
    for pdf in pdfs:
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"  📄 {pdf.name} ({size_mb:.2f} MB)")

def show_expected_results():
    """Show what we expect from the realistic PDFs"""
    print("\n" + "="*80)
    print("EXPECTED RESULTS FOR REALISTIC PDFs")
    print("="*80)
    
    expected = [
        {
            "file": "Realistic_IIT_A+_SSR.pdf",
            "grade": "A+",
            "confidence": "75-85%",
            "chunks": "40-60 (MORE chunks due to detailed tables)",
            "projects": "458 projects",
            "funding": "₹18000 Lakhs"
        },
        {
            "file": "Realistic_State_University_B+_SSR.pdf",
            "grade": "B+",
            "confidence": "55-65%",
            "chunks": "15-25 (FEWER chunks, less detail)",
            "projects": "108 projects",
            "funding": "₹2500 Lakhs"
        },
        {
            "file": "Realistic_Regional_College_C_SSR.pdf",
            "grade": "C",
            "confidence": "25-35%",
            "chunks": "8-15 (MINIMAL chunks)",
            "projects": "14 projects",
            "funding": "₹220 Lakhs"
        }
    ]
    
    for exp in expected:
        print(f"\n📄 {exp['file']}")
        print(f"   Expected Grade: {exp['grade']}")
        print(f"   Expected Confidence: {exp['confidence']}")
        print(f"   Expected Chunks: {exp['chunks']}")
        print(f"   Data: {exp['projects']}, {exp['funding']}")

if __name__ == "__main__":
    check_raw_pdfs()
    analyze_current_chunks()
    show_expected_results()
    
    print("\n" + "="*80)
    print("TESTING INSTRUCTIONS")
    print("="*80)
    print("\n1. Run: python nuclear_clear.py")
    print("2. Upload B+ PDF via website")
    print("3. Click 'Ingest Files'")
    print("4. Run: python compare_pdf_chunks.py")
    print("5. Note the chunk count")
    print("6. Run audit and note grade/confidence")
    print("7. Repeat steps 1-6 with A+ PDF")
    print("8. Compare: A+ should have MORE chunks than B+")
    print("\n" + "="*80)
