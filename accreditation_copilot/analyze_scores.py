"""Analyze scores by source type"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scoring.evidence_scorer import EvidenceScorer
from scoring.confidence_calculator import ConfidenceCalculator
from retrieval.dual_retrieval import DualRetriever
from models.model_manager import get_model_manager

# Initialize
model_manager = get_model_manager()
retriever = DualRetriever(model_manager=model_manager)
scorer = EvidenceScorer()

# Query for 3.2.1
query = "extramural research funding amount lakhs projects DST SERB DBT ICSSR government agencies year-wise"

# Retrieve
results, _ = retriever.retrieve(
    query=query,
    query_variants=[query],
    framework="NAAC",
    query_type='metric',
    top_k_framework=3,
    top_k_institution=7
)

# Score
evidence_scores = scorer.score(results)

# Separate by source type
institution_scores = []
framework_scores = []

for result, score_data in zip(results, evidence_scores):
    source_type = result.get('source_type', 'unknown')
    reranker = result.get('reranker_score', 0)
    evidence = score_data['evidence_score']
    
    data = {
        'source': result.get('source', 'unknown'),
        'reranker': reranker,
        'evidence': evidence,
        'combined': (0.6 * evidence + 0.4 * reranker)  # Same formula as confidence calculator
    }
    
    if source_type == 'institution':
        institution_scores.append(data)
    else:
        framework_scores.append(data)

print("\n" + "="*80)
print("SCORE ANALYSIS BY SOURCE TYPE")
print("="*80)

print(f"\nINSTITUTION CHUNKS ({len(institution_scores)}):")
for i, data in enumerate(institution_scores, 1):
    print(f"  {i}. {data['source']}")
    print(f"     Reranker: {data['reranker']:.3f} | Evidence: {data['evidence']:.3f} | Combined: {data['combined']:.3f}")

if institution_scores:
    avg_inst_reranker = sum(d['reranker'] for d in institution_scores) / len(institution_scores)
    avg_inst_evidence = sum(d['evidence'] for d in institution_scores) / len(institution_scores)
    avg_inst_combined = sum(d['combined'] for d in institution_scores) / len(institution_scores)
    print(f"\n  AVERAGES:")
    print(f"    Reranker: {avg_inst_reranker:.3f}")
    print(f"    Evidence: {avg_inst_evidence:.3f}")
    print(f"    Combined: {avg_inst_combined:.3f}")

print(f"\nFRAMEWORK CHUNKS ({len(framework_scores)}):")
for i, data in enumerate(framework_scores, 1):
    print(f"  {i}. {data['source']}")
    print(f"     Reranker: {data['reranker']:.3f} | Evidence: {data['evidence']:.3f} | Combined: {data['combined']:.3f}")

if framework_scores:
    avg_fw_reranker = sum(d['reranker'] for d in framework_scores) / len(framework_scores)
    avg_fw_evidence = sum(d['evidence'] for d in framework_scores) / len(framework_scores)
    avg_fw_combined = sum(d['combined'] for d in framework_scores) / len(framework_scores)
    print(f"\n  AVERAGES:")
    print(f"    Reranker: {avg_fw_reranker:.3f}")
    print(f"    Evidence: {avg_fw_evidence:.3f}")
    print(f"    Combined: {avg_fw_combined:.3f}")

print("\n")
