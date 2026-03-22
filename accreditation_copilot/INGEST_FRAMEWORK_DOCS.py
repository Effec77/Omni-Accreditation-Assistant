"""
Ingest Framework Documents - Build framework indexes from NAAC/NBA PDFs
This will populate the empty framework indexes with actual NAAC/NBA criteria data.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from ingestion.run_ingestion import IngestionOrchestrator

def main():
    print("\n" + "="*80)
    print("FRAMEWORK DOCUMENT INGESTION")
    print("="*80)
    
    # Use the actual PDF locations on D: drive
    naac_dir = "D:/Accreditation Frameworks/NAAC"
    nba_dir = "D:/Accreditation Frameworks/NBA"
    
    print(f"\nIngesting framework documents from:")
    print(f"  NAAC: {naac_dir}")
    print(f"  NBA: {nba_dir}")
    
    # Check if directories exist
    if not Path(naac_dir).exists():
        print(f"\n❌ ERROR: NAAC directory not found: {naac_dir}")
        print("Please update the path in this script to match your system.")
        return
    
    if not Path(nba_dir).exists():
        print(f"\n❌ ERROR: NBA directory not found: {nba_dir}")
        print("Please update the path in this script to match your system.")
        return
    
    print("\n✓ Directories found")
    print("\nStarting ingestion...")
    print("This will:")
    print("  1. Process all NAAC PDFs")
    print("  2. Process all NBA PDFs")
    print("  3. Create framework indexes (FAISS + BM25)")
    print("  4. Store chunks in metadata.db")
    
    try:
        orchestrator = IngestionOrchestrator()
        orchestrator.run(naac_dir=naac_dir, nba_dir=nba_dir)
        
        print("\n" + "="*80)
        print("✓ FRAMEWORK INGESTION COMPLETE")
        print("="*80)
        
        # Verify framework chunks were created
        import sqlite3
        conn = sqlite3.connect('accreditation_copilot/data/metadata.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="framework"')
        framework_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM chunks WHERE source_type="institution"')
        institution_count = cursor.fetchone()[0]
        
        print(f"\nChunk counts:")
        print(f"  Framework chunks: {framework_count}")
        print(f"  Institution chunks: {institution_count}")
        
        if framework_count > 0:
            print("\n✓ SUCCESS: Framework indexes now have data!")
            print("\nYou can now test all 11 NAAC criteria.")
        else:
            print("\n❌ WARNING: No framework chunks created")
            print("Check if the NAAC/NBA PDFs are in the correct directories.")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERROR during ingestion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
