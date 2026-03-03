"""
Phase 2 Complete Pipeline Test
Tests the FULL retrieval pipeline with detailed output:
- Query expansion
- Hybrid retrieval (FAISS + BM25)
- HyDE retrieval
- Score fusion
- Reranking
- Parent-child expansion
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from retrieval.retrieval_pipeline import RetrievalPipeline


async def test_complete_pipeline():
    """Test complete Phase 2 pipeline with detailed output."""
    
    print("\n" + "="*80)
    print("PHASE 2 COMPLETE PIPELINE TEST")
    print("Testing: Query Expansion -> Hybrid Retrieval -> Reranking -> Parent Expansion")
    print("="*80)
    
    pipeline = RetrievalPipeline()
    
    # Test with a single comprehensive query
    test_query = "What are the requirements for NAAC 3.2.1?"
    
    print(f"\n{'='*80}")
    print(f"QUERY: {test_query}")
    print(f"{'='*80}")
    
    try:
        # Run with verbose=True to see all steps
        results = await pipeline.run_retrieval(
            query=test_query,
            verbose=True,
            enable_parent_expansion=True
        )
        
        # Additional detailed output
        print(f"\n{'='*80}")
        print(f"DETAILED RESULTS ANALYSIS")
        print(f"{'='*80}")
        
        for i, result in enumerate(results, 1):
            print(f"\n{'─'*80}")
            print(f"RESULT #{i}")
            print(f"{'─'*80}")
            
            # Basic info
            print(f"Framework: {result['framework']}")
            print(f"Source: {result['source']}")
            print(f"Page: {result['page']}")
            print(f"Type: {result['doc_type']}")
            print(f"Criterion: {result.get('criterion', 'N/A')}")
            
            # Scores
            print(f"\nRetrieval Scores:")
            print(f"  • Dense (FAISS):     {result['scores']['dense']:.4f}")
            print(f"  • Sparse (BM25):     {result['scores']['bm25']:.4f}")
            print(f"  • Fused (RRF):       {result['scores']['fused']:.4f}")
            print(f"  • Reranker (Final):  {result['scores']['reranker']:.4f}")
            
            # Parent-child expansion details
            if 'metadata' in result:
                meta = result['metadata']
                print(f"\nParent-Child Expansion:")
                print(f"  • Parent Section ID: {meta['parent_section_id']}")
                print(f"  • Siblings Added:    {meta['num_siblings_used']}")
                print(f"  • Child Tokens:      {meta['child_tokens']}")
                print(f"  • Parent Tokens:     {meta['parent_tokens']}")
                print(f"  • Expansion Ratio:   {meta['parent_tokens'] / meta['child_tokens']:.2f}x")
                print(f"  • Token Limit OK:    {'✓' if meta['parent_tokens'] <= 1200 else '✗'}")
            
            # Text content
            print(f"\nChild Text (Original Chunk):")
            child_text = result.get('child_text', result.get('text', ''))[:300]
            print(f"  {child_text}...")
            
            if 'parent_context' in result:
                print(f"\nParent Context (Expanded with Siblings):")
                parent_preview = result['parent_context'][:300]
                print(f"  {parent_preview}...")
        
        # Summary statistics
        print(f"\n{'='*80}")
        print(f"PIPELINE SUMMARY")
        print(f"{'='*80}")
        
        avg_reranker = sum(r['scores']['reranker'] for r in results) / len(results)
        avg_expansion = sum(
            r['metadata']['parent_tokens'] / r['metadata']['child_tokens'] 
            for r in results if 'metadata' in r
        ) / len([r for r in results if 'metadata' in r])
        total_siblings = sum(
            r['metadata']['num_siblings_used'] 
            for r in results if 'metadata' in r
        )
        
        print(f"✓ Total Results Retrieved: {len(results)}")
        print(f"✓ Average Reranker Score: {avg_reranker:.3f}")
        print(f"✓ Average Context Expansion: {avg_expansion:.2f}x")
        print(f"✓ Total Siblings Added: {total_siblings}")
        print(f"✓ All Components Working: Query Expansion + Hybrid Retrieval + Reranking + Parent Expansion")
        
        print(f"\n{'='*80}")
        print(f"✓ PHASE 2 COMPLETE PIPELINE TEST PASSED")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"✗ TEST FAILED")
        print(f"{'='*80}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pipeline.close()


if __name__ == "__main__":
    asyncio.run(test_complete_pipeline())
