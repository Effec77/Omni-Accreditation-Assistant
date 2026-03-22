"""
Debug script to understand why full audit is giving 0 scores
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "accreditation_copilot"))

from audit.criterion_auditor import CriterionAuditor
from models.model_manager import get_model_manager
from criteria.criterion_registry import get_criteria
from scoring.naac_grading import calculate_naac_cgpa

print("=" * 80)
print("DEBUGGING FULL AUDIT SCORING ISSUE")
print("=" * 80)

# Initialize
model_manager = get_model_manager()
auditor = CriterionAuditor(model_manager=model_manager)

# Get all NAAC criteria
naac_criteria = get_criteria("NAAC")
print(f"\nTotal NAAC criteria: {len(naac_criteria)}")

# Test first criterion in detail
test_criterion = naac_criteria[0]
print(f"\n{'='*80}")
print(f"TESTING CRITERION: {test_criterion['criterion']}")
print(f"Description: {test_criterion['description']}")
print(f"Query Template: {test_criterion['query_template']}")
print(f"{'='*80}")

try:
    result = auditor.audit_criterion(
        criterion_id=test_criterion['criterion'],
        framework="NAAC",
        query_template=test_criterion['query_template'],
        description=test_criterion['description'],
        user_query=""
    )
    
    print(f"\n📊 AUDIT RESULT:")
    print(f"   Confidence Score: {result.get('confidence_score', 0):.3f}")
    print(f"   Coverage Ratio: {result.get('coverage_ratio', 0):.3f}")
    print(f"   Compliance Status: {result.get('compliance_status', 'unknown')}")
    print(f"   Evidence Count: {result.get('evidence_count', 0)}")
    print(f"   Institution Evidence Count: {result.get('institution_evidence_count', 0)}")
    print(f"   Framework Evidence Count: {result.get('framework_evidence_count', 0)}")
    
    # Check dimensions
    dims_covered = result.get('dimensions_covered', [])
    dims_missing = result.get('dimensions_missing', [])
    print(f"\n📋 DIMENSIONS:")
    print(f"   Covered: {len(dims_covered)}")
    print(f"   Missing: {len(dims_missing)}")
    
    if dims_covered:
        print(f"\n   Covered dimensions (first 3):")
        for dim in dims_covered[:3]:
            print(f"      - {dim}")
    
    if dims_missing:
        print(f"\n   Missing dimensions (first 3):")
        for dim in dims_missing[:3]:
            print(f"      - {dim}")
    
    # Check evidence
    evidence = result.get('evidence_sources', [])
    print(f"\n📄 EVIDENCE:")
    print(f"   Total evidence chunks: {len(evidence)}")
    if evidence:
        print(f"\n   First evidence chunk:")
        first_ev = evidence[0]
        print(f"      Source: {first_ev.get('source', 'unknown')}")
        print(f"      Type: {first_ev.get('source_type', 'unknown')}")
        print(f"      Content preview: {first_ev.get('content', '')[:100]}...")
    
    # Check gaps
    gaps = result.get('gaps', [])
    print(f"\n⚠️  GAPS:")
    print(f"   Total gaps: {len(gaps)}")
    if gaps:
        print(f"\n   First 3 gaps:")
        for gap in gaps[:3]:
            print(f"      - {gap}")
    
    print(f"\n{'='*80}")
    print("DIAGNOSIS:")
    print(f"{'='*80}")
    
    if result.get('institution_evidence_count', 0) == 0:
        print("❌ CRITICAL: No institution evidence found!")
        print("   This means the SSR document chunks are not being retrieved.")
        print("   Possible causes:")
        print("   1. Institution chunks not in database")
        print("   2. Query template not matching institution content")
        print("   3. Embedding/retrieval issue")
    
    if result.get('framework_evidence_count', 0) == 0:
        print("❌ CRITICAL: No framework evidence found!")
        print("   This means NAAC framework chunks are not being retrieved.")
        print("   Possible causes:")
        print("   1. Framework chunks not in database")
        print("   2. Query template not matching framework content")
    
    if result.get('confidence_score', 0) < 0.1:
        print("❌ CRITICAL: Confidence score near zero!")
        print("   This indicates the scoring logic is broken or no valid comparison.")
    
    if len(dims_covered) == 0:
        print("❌ CRITICAL: No dimensions covered!")
        print("   This means the LLM didn't identify any matching dimensions.")
    
except Exception as e:
    print(f"\n❌ ERROR during audit: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
print("NEXT STEPS:")
print(f"{'='*80}")
print("1. Check if institution chunks exist in database")
print("2. Check if framework chunks exist in database")
print("3. Test retrieval with sample query")
print("4. Check LLM scoring logic")
