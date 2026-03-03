"""
Phase 2 Precision Upgrade Test
Tests explicit metric retrieval with precision fixes.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from retrieval.retrieval_pipeline import RetrievalPipeline


async def test_precision():
    """Test precision upgrades for explicit metric queries."""
    
    print("\n" + "="*80)
    print("PHASE 2 PRECISION UPGRADE TEST")
    print("="*80)
    
    pipeline = RetrievalPipeline()
    
    test_cases = [
        {
            'name': 'NAAC 3.2.1',
            'query': 'What are the requirements for NAAC 3.2.1?',
            'expected_criterion': '3.2.1',
            'expected_framework': 'NAAC'
        },
        {
            'name': 'NBA Faculty (C5)',
            'query': 'What are the minimum faculty requirements for NBA Tier-II?',
            'expected_criterion': 'C5',
            'expected_framework': 'NBA'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'='*80}")
        print(f"Query: {test_case['query']}\n")
        
        try:
            results = await pipeline.run_retrieval(
                query=test_case['query'],
                verbose=True,
                enable_parent_expansion=True
            )
            
            # Validation
            print(f"\n{'='*80}")
            print(f"VALIDATION")
            print(f"{'='*80}")
            
            # Check reranker score spread
            reranker_scores = [r['scores']['reranker'] for r in results]
            score_spread = max(reranker_scores) - min(reranker_scores)
            
            print(f"[+] Reranker Score Spread: {score_spread:.3f} (min={min(reranker_scores):.3f}, max={max(reranker_scores):.3f})")
            
            if score_spread >= 0.4:
                print(f"  [+] Meaningful spread (>= 0.4)")
            else:
                print(f"  [!] Low spread (< 0.4) - may indicate saturation")
            
            # Check if scores are saturated near 1.0
            if max(reranker_scores) > 0.95 and score_spread < 0.2:
                print(f"  [!] Scores saturated near 1.0")
            else:
                print(f"  [+] No saturation")
            
            # Check criterion match
            criteria = [r.get('criterion') for r in results]
            print(f"\n[+] Top-5 Criteria: {criteria}")
            
            if test_case.get('expected_criterion'):
                if criteria[0] == test_case['expected_criterion']:
                    print(f"  [+] Exact match at rank 1: {criteria[0]}")
                elif test_case['expected_criterion'] in criteria:
                    rank = criteria.index(test_case['expected_criterion']) + 1
                    print(f"  [!] Exact match at rank {rank}: {test_case['expected_criterion']}")
                else:
                    print(f"  [X] Exact match not in top-5: {test_case['expected_criterion']}")
            
            # Check framework
            frameworks = set(r['framework'] for r in results)
            if test_case['expected_framework'] in frameworks:
                print(f"  [+] Framework: {test_case['expected_framework']}")
            
            print(f"\n[+] TEST CASE {i} COMPLETED")
            
        except Exception as e:
            print(f"\n[X] ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    pipeline.close()
    
    print(f"\n{'='*80}")
    print(f"PRECISION TEST COMPLETE")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(test_precision())
