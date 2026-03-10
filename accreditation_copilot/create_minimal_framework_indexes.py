"""
Create minimal framework indexes to allow the system to run.
This creates empty indexes that won't break the retrieval system.
"""
import sys
from pathlib import Path
import numpy as np
import faiss
import pickle

sys.path.insert(0, str(Path(__file__).parent))

from models.model_manager import get_model_manager

def create_minimal_indexes():
    """Create minimal framework indexes."""
    
    # Get embedder to know the dimension
    model_manager = get_model_manager()
    embedder = model_manager.get_embedder()
    
    # Get embedding dimension
    test_embedding = embedder.encode(["test"])
    dimension = test_embedding.shape[1]
    
    print(f"Embedding dimension: {dimension}")
    
    # Create indexes directory
    indexes_dir = Path("api/indexes/framework")
    indexes_dir.mkdir(parents=True, exist_ok=True)
    
    # Framework index types
    index_types = [
        'naac_metric',
        'naac_policy',
        'nba_metric',
        'nba_policy',
        'nba_prequalifier'
    ]
    
    for index_type in index_types:
        print(f"\nCreating {index_type} indexes...")
        
        # Create empty FAISS index
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_path = indexes_dir / f"{index_type}.index"
        faiss.write_index(faiss_index, str(faiss_path))
        print(f"  Created FAISS index: {faiss_path}")
        
        # Create empty BM25 index
        bm25_data = {
            'index': None,  # Empty BM25 index
            'chunk_ids': [],
            'chunks': []
        }
        bm25_path = indexes_dir / f"{index_type}_bm25.pkl"
        with open(bm25_path, 'wb') as f:
            pickle.dump(bm25_data, f)
        print(f"  Created BM25 index: {bm25_path}")
        
        # Create empty mapping
        mapping = {
            'chunk_ids': [],
            'chunks': []
        }
        mapping_path = indexes_dir / f"{index_type}_mapping.pkl"
        with open(mapping_path, 'wb') as f:
            pickle.dump(mapping, f)
        print(f"  Created mapping: {mapping_path}")
    
    print(f"\n✓ All framework indexes created successfully!")
    print(f"  Location: {indexes_dir.absolute()}")
    print(f"\nNote: These are empty indexes. The system will work but won't have")
    print(f"framework guidelines. To add framework data, place NAAC/NBA PDFs in:")
    print(f"  - data/raw_docs/naac/")
    print(f"  - data/raw_docs/nba/")
    print(f"Then run: python ingestion/run_ingestion.py")

if __name__ == "__main__":
    create_minimal_indexes()
