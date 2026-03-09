import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from audit.criterion_auditor import CriterionAuditor
from criteria.criterion_registry import get_criteria

# Get criterion details
criteria = get_criteria('NAAC')
criterion_def = next((c for c in criteria if c['criterion'] == '3.2.1'), None)

print(f"Criterion: {criterion_def['criterion']}")
print(f"Description: {criterion_def['description']}")
print(f"Query: {criterion_def['query_template']}\n")

# Run audit
auditor = CriterionAuditor()
result = auditor.audit_criterion(
    criterion_id='3.2.1',
    framework='NAAC',
    query_template=criterion_def['query_template'],
    description=criterion_def['description']
)

print(f"Compliance Status: {result['compliance_status']}")
print(f"Confidence Score: {result['confidence_score']}")
print(f"Coverage Ratio: {result['coverage_ratio']}")
print(f"Evidence Count: {result['evidence_count']}")
print(f"Institution Evidence Count: {result['institution_evidence_count']}")
print(f"Institution Evidence Available: {result['institution_evidence_available']}")

# Check the full report for more details
full_report = result.get('full_report', {})
confidence_details = full_report.get('confidence', {})
print(f"\nConfidence Details:")
print(f"  Base Score: {confidence_details.get('base_score', 0)}")
print(f"  Avg Evidence Score: {confidence_details.get('avg_evidence_score', 0)}")
print(f"  Avg Retrieval Score: {confidence_details.get('avg_retrieval_score', 0)}")

# Check evidence sources
print(f"\nEvidence Sources (first 3):")
for i, source in enumerate(result.get('evidence_sources', [])[:3], 1):
    print(f"{i}. {source.get('chunk_id', 'N/A')[:50]}... - {source.get('source_type', 'N/A')}")
