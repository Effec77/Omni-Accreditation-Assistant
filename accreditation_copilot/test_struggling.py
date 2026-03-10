"""Test audit for Struggling College"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from audit.criterion_auditor import CriterionAuditor

auditor = CriterionAuditor()

result = auditor.audit_criterion(
    criterion_id="3.2.1",
    framework="NAAC",
    query_template="extramural research funding amount lakhs projects DST SERB DBT ICSSR government agencies year-wise",
    description="Extramural funding for Research"
)

print("\n" + "="*80)
print("STRUGGLING COLLEGE AUDIT RESULT")
print("="*80)
print(f"Confidence Score: {result['confidence_score']:.3f}")
print(f"Compliance Status: {result['compliance_status']}")
print(f"Coverage Ratio: {result['coverage_ratio']:.3f}")
print(f"Dimensions Covered: {result['dimensions_covered']}")
print(f"Dimensions Missing: {result['dimensions_missing']}")

print(f"\nTop Evidence Sources:")
for i, source in enumerate(result.get('evidence_sources', [])[:5], 1):
    src_name = source.get('source', 'unknown')
    score = source.get('reranker_score', 0)
    print(f"  {i}. {src_name} - Reranker: {score:.3f}")

print("\n")
