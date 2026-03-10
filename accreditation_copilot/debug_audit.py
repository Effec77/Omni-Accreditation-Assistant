"""Debug script to see what's happening in the audit for Excellence University"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from audit.full_audit_runner import FullAuditRunner
import json

if __name__ == "__main__":
    runner = FullAuditRunner()
    
    # Run audit for NAAC framework (includes 3.2.1)
    result = runner.run_audit(
        framework="NAAC",
        institution_name="Excellence University",
        save_results=False
    )
    
    # Find 3.2.1 result
    criterion_result = None
    for cr in result['criteria_results']:
        if cr['criterion'] == '3.2.1':
            criterion_result = cr
            break
    
    if criterion_result:
        print("\n" + "="*80)
        print("AUDIT RESULT FOR NAAC 3.2.1")
        print("="*80)
        print(f"Confidence Score: {criterion_result['confidence_score']}")
        print(f"Coverage Ratio: {criterion_result['coverage_ratio']}")
        print(f"Dimensions Covered: {criterion_result['dimensions_covered']}")
        print(f"Dimensions Missing: {criterion_result['dimensions_missing']}")
        print(f"Evidence Count: {criterion_result['evidence_count']}")
        print(f"Institution Evidence Count: {criterion_result['institution_evidence_count']}")
        print(f"Compliance Status: {criterion_result['compliance_status']}")
        
        # Print confidence breakdown from full_report
        full_report = criterion_result.get('full_report', {})
        print(f"\nConfidence Breakdown (from full_report):")
        print(f"  Base Score: {full_report.get('base_score', 0):.3f}")
        print(f"  Avg Evidence Score: {full_report.get('avg_evidence_score', 0):.3f}")
        print(f"  Avg Retrieval Score: {full_report.get('avg_retrieval_score', 0):.3f}")
        
        # Print evidence sources
        print(f"\nTop 5 Evidence Sources:")
        for i, source in enumerate(criterion_result.get('evidence_sources', [])[:5], 1):
            print(f"  {i}. {source.get('source', 'unknown')} - Reranker: {source.get('reranker_score', 0):.3f}")
    else:
        print("ERROR: Could not find 3.2.1 result")
    
    print("\n")
