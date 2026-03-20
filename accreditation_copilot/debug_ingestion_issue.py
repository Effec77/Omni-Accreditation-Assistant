"""
Debug script to investigate ingestion and chunking issues
"""
import sqlite3
from pathlib import Path
from collections import Counter

def check_database_chunks():
    """Check what chunks are in the database"""
    db_path = Path("data/metadata.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get all institution chunks
    cursor.execute("""
        SELECT chunk_id, source, page, framework, criterion, doc_type, 
               substr(text, 1, 100) as text_preview
        FROM chunks 
        WHERE source_type='institution'
        ORDER BY source, page
    """)
    
    chunks = cursor.fetchall()
    
    print(f"\n{'='*80}")
    print(f"DATABASE CHUNKS ANALYSIS")
    print(f"{'='*80}")
    print(f"Total institution chunks: {len(chunks)}")
    
    if not chunks:
        print("\n❌ No institution chunks found in database!")
        conn.close()
        return
    
    # Group by source
    sources = Counter([c[1] for c in chunks])
    print(f"\nChunks by source:")
    for source, count in sources.items():
        print(f"  {source}: {count} chunks")
    
    # Show first few chunks from each source
    print(f"\n{'='*80}")
    print(f"CHUNK DETAILS")
    print(f"{'='*80}")
    
    current_source = None
    for chunk in chunks[:20]:  # Show first 20
        chunk_id, source, page, framework, criterion, doc_type, text_preview = chunk
        
        if source != current_source:
            current_source = source
            print(f"\n📄 Source: {source}")
            print(f"{'─'*80}")
        
        print(f"  Chunk ID: {chunk_id}")
        print(f"  Page: {page} | Type: {doc_type} | Criterion: {criterion or 'None'}")
        print(f"  Text: {text_preview}...")
        print()
    
    conn.close()

def check_index_files():
    """Check what index files exist"""
    indexes_dir = Path("indexes/institution")
    
    print(f"\n{'='*80}")
    print(f"INDEX FILES")
    print(f"{'='*80}")
    
    if not indexes_dir.exists():
        print("❌ Indexes directory not found!")
        return
    
    files = list(indexes_dir.glob("institution*"))
    
    if not files:
        print("❌ No institution index files found!")
        return
    
    print(f"Found {len(files)} index files:")
    for file in files:
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name} ({size_kb:.1f} KB)")

def check_raw_docs():
    """Check what PDFs are in raw_docs"""
    raw_docs_dir = Path("data/raw_docs")
    
    print(f"\n{'='*80}")
    print(f"RAW DOCUMENTS")
    print(f"{'='*80}")
    
    if not raw_docs_dir.exists():
        print("❌ Raw docs directory not found!")
        return
    
    pdfs = list(raw_docs_dir.glob("*.pdf"))
    
    if not pdfs:
        print("❌ No PDFs found in raw_docs!")
        return
    
    print(f"Found {len(pdfs)} PDF(s):")
    for pdf in pdfs:
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"  {pdf.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    check_raw_docs()
    check_database_chunks()
    check_index_files()
    
    print(f"\n{'='*80}")
    print(f"DIAGNOSIS COMPLETE")
    print(f"{'='*80}")
