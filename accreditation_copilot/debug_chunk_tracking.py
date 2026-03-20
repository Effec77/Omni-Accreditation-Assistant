"""
Debug script to track chunk creation and verify cache clearing
"""
import sqlite3
from pathlib import Path
from collections import Counter
import json

def analyze_chunks_detailed():
    """Detailed analysis of chunks in database"""
    db_path = Path("data/metadata.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get all chunks with full details
    cursor.execute("""
        SELECT chunk_id, source, page, framework, criterion, doc_type, text
        FROM chunks 
        WHERE source_type='institution'
        ORDER BY chunk_id
    """)
    
    chunks = cursor.fetchall()
    
    print(f"\n{'='*80}")
    print(f"DETAILED CHUNK ANALYSIS")
    print(f"{'='*80}")
    print(f"Total institution chunks: {len(chunks)}")
    
    if not chunks:
        print("\n✅ Database is clean - no institution chunks found")
        conn.close()
        return
    
    # Analyze by source
    sources = Counter([c[1] for c in chunks])
    print(f"\n📊 Chunks by Source:")
    for source, count in sources.most_common():
        print(f"  {source}: {count} chunks")
    
    # Analyze by doc_type
    doc_types = Counter([c[5] for c in chunks])
    print(f"\n📄 Chunks by Document Type:")
    for doc_type, count in doc_types.most_common():
        print(f"  {doc_type}: {count} chunks")
    
    # Show all chunks with details
    print(f"\n{'='*80}")
    print(f"ALL CHUNKS (showing first 100 chars of text)")
    print(f"{'='*80}")
    
    for i, chunk in enumerate(chunks, 1):
        chunk_id, source, page, framework, criterion, doc_type, text = chunk
        text_preview = text[:100].replace('\n', ' ')
        
        print(f"\n{i}. Chunk ID: {chunk_id}")
        print(f"   Source: {source}")
        print(f"   Page: {page} | Type: {doc_type}")
        print(f"   Text: {text_preview}...")
    
    conn.close()
    
    # Check if chunks are duplicates
    print(f"\n{'='*80}")
    print(f"DUPLICATE CHECK")
    print(f"{'='*80}")
    
    chunk_texts = [c[6] for c in chunks]
    unique_texts = set(chunk_texts)
    
    if len(chunk_texts) == len(unique_texts):
        print("✅ No duplicate chunks found")
    else:
        duplicates = len(chunk_texts) - len(unique_texts)
        print(f"⚠️  Found {duplicates} duplicate chunks!")
        
        # Find which texts are duplicated
        text_counts = Counter(chunk_texts)
        print("\nDuplicated texts:")
        for text, count in text_counts.items():
            if count > 1:
                print(f"  - Appears {count} times: {text[:80]}...")

def clear_all_institution_data():
    """Completely clear all institution data"""
    print(f"\n{'='*80}")
    print(f"CLEARING ALL INSTITUTION DATA")
    print(f"{'='*80}")
    
    # Clear database
    db_path = Path("data/metadata.db")
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.execute("DELETE FROM chunks WHERE source_type='institution'")
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        print(f"✅ Deleted {deleted} chunks from database")
    
    # Clear indexes
    indexes_dir = Path("indexes/institution")
    if indexes_dir.exists():
        deleted_files = []
        for file in indexes_dir.glob("institution*"):
            file.unlink()
            deleted_files.append(file.name)
        print(f"✅ Deleted {len(deleted_files)} index files")
        for f in deleted_files:
            print(f"   - {f}")
    
    # Clear audit cache
    from cache.audit_cache import AuditCache
    cache = AuditCache()
    cache.clear_cache()
    print(f"✅ Cleared audit cache")
    
    print(f"\n{'='*80}")
    print(f"ALL INSTITUTION DATA CLEARED")
    print(f"{'='*80}")
    print("\nNow you can upload a fresh PDF and ingest it.")

def check_raw_pdfs():
    """Check what PDFs are currently in raw_docs"""
    raw_docs = Path("data/raw_docs")
    
    print(f"\n{'='*80}")
    print(f"CURRENT PDFs IN RAW_DOCS")
    print(f"{'='*80}")
    
    if not raw_docs.exists():
        print("❌ raw_docs directory not found")
        return
    
    pdfs = list(raw_docs.glob("*.pdf"))
    
    if not pdfs:
        print("✅ No PDFs in raw_docs (clean state)")
        return
    
    print(f"Found {len(pdfs)} PDF(s):")
    for pdf in pdfs:
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"  📄 {pdf.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_all_institution_data()
    else:
        check_raw_pdfs()
        analyze_chunks_detailed()
        
        print(f"\n{'='*80}")
        print(f"USAGE")
        print(f"{'='*80}")
        print("To clear all data: python debug_chunk_tracking.py --clear")
        print("To analyze: python debug_chunk_tracking.py")
