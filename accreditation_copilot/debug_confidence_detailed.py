"""Debug confidence calculation with detailed output"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scoring.evidence_scorer import EvidenceScorer
from scoring.dimension_checker import DimensionChecker
from scoring.confidence_calculator import ConfidenceCalculator
from retrieval.dual_retrieval import DualRetriever
from models.model_manager import get_model_manager

# Initialize
model_manager = get_model_manager()
retriever = DualRetriever(model_manager=model_manager)
scorer = EvidenceScorer()
checker = DimensionChecker()
calculator = ConfidenceCalculator()

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

print("\n" + "="*80)
print("DETAILED CONFIDENCE DEBUG")
print("="*80)

print(f"\nTotal chunks retrieved: {len(results)}")

# Check source types
institution_count = sum(1 for r in results if r.get('source_type') == 'institution')
framework_count = sum(1 for r in results if r.get('source_type') == 'framework')

print(f"Institution chunks: {institution_count}")
print(f"Framework chunks: {framework_count}")

# Score
evidence_scores = scorer.score(results)

print(f"\nEvidence Scores:")
for i, (result, score_data) in enumerate(zip(results, evidence_scores), 1):
    source_type = result.get('source_type', 'unknown')
    reranker = result.get('reranker_score', 0)
    evidence = score_data['evidence_score']
    print(f"  {i}. {source_type:12} - Reranker: {reranker:.3f}, Evidence: {evidence:.3f}")

# Check coverage
coverage = checker.check(results, "NAAC", "3.2.1")

# Calculate confidence
confidence = calculator.calculate(evidence_scores, coverage, results)

print(f"\nConfidence Calculation:")
print(f"  Avg Evidence Score: {confidence['avg_evidence_score']:.3f}")
print(f"  Avg Retrieval Score: {confidence['avg_retrieval_score']:.3f}")
print(f"  Base Score: {confidence['base_score']:.3f}")
print(f"  Coverage Ratio: {confidence['coverage_ratio']:.3f}")
print(f"  Final Confidence Score: {confidence['confidence_score']:.3f}")
print(f"  Status: {confidence['status']}")

print("\n")
