"""
Diagnose why Full NAAC Audit is giving low scores (0.36 CGPA)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "accreditation_copilot"))

from audit.criterion_auditor import CriterionAuditor
from models.model_manager import get_model_manager
from criteria.criterion_registry import get_criteria

print("=" * 80)
print("DIAGNOSING LOW SCORES IN FULL NAAC AUDIT")
print("=" * 80)

# Initialize
model_manager = get_model_manager()
auditor = CriterionAuditor(model_manager=model_manager)

# Get all NAAC criteria
naac_criteria = get_criteria("NAAC")

# Test first 3 criteria to see the pattern
print(f"\nTesting first 3 criteria to identify the issue...")

for i, criterion_def in enumerate(naac_criteria[:3], 1):
    criterion_id = criterion_def['criterion']
    
    print(f"\n{'='*80}")
    print(f"CRITERION {i}: {criterion_id}")
    print(f"{'='*80}")
    
    try:
        result = auditor.audit_criterion(
            criterion_id=criterion_id,
            framework="NAAC",
            query_template=criterion_def['query_template'],
            description=criterion_def['description'],
            user_query=""
        )
        
        confidence = result.get('confidence_score', 0)
        coverage = result.get('coverage_ratio', 0)
        inst_count = result.get('institution_evidence_count', 0)
        frame_count = result.get('framework_evidence_count', 0)
        
        print(f"\n📊 SCORES:")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   Coverage: {coverage:.3f}")
        
        print(f"\n📄 EVIDENCE:")
        print(f"   Institution chunks: {inst_count}")
        print(f"   Framework chunks: {frame_count}")
        
        # Check gaps
        gaps = result.get('gaps', [])
        print(f"\n⚠️  GAPS ({len(gaps)}):")
        for gap in gaps[:3]:
            print(f"   - {gap}")
        
        # Diagnosis
        print(f"\n🔍 DIAGNOSIS:")
        if confidence < 0.1:
            print("   ❌ CRITICAL: Confidence near zero")
            if "Synthesis generation failed" in str(gaps):
                print("      → LLM synthesis failed (likely rate limit)")
            elif inst_count == 0:
                print("      → No institution evidence found")
            elif frame_count == 0:
                print("      → No framework evidence found")
            else:
                print("      → Scoring logic issue")
        elif confidence < 0.3:
            print("   ⚠️  WARNING: Very low confidence")
            print("      → Evidence quality may be poor")
            print("      → Or scoring is too strict")
        else:
            print("   ✅ Confidence is reasonable")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nIf all criteria show:")
print("- Confidence near 0: LLM synthesis is failing (rate limit or API issue)")
print("- Low confidence (0.1-0.3): Scoring logic is too strict or evidence is poor")
print("- Reasonable confidence (>0.3): System is working, but document quality varies")
print()
print("Expected for A+ document: Confidence 0.6-0.9 for most criteria")
print("Current CGPA 0.36 suggests: Most criteria have confidence 0.1-0.2")
print()
