"""Debug confidence calculation"""
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

# Score
evidence_scores = scorer.score(results)

# Check coverage
coverage = checker.check(results, "NAAC", "3.2.1")

# Calculate confidence
confidence = calculator.calculate(evidence_scores, coverage, results)

print("\n" + "="*80)
print("CONFIDENCE CALCULATION DEBUG")
print("="*80)

print(f"\nEvidence Scores ({len(evidence_scores)} chunks):")
for i, score_data in enumerate(evidence_scores[:10], 1):
    print(f"  {i}. Chunk {score_data['chunk_id'][:8]}... - Evidence Score: {score_data['evidence_score']:.3f}")

print(f"\nCoverage:")
print(f"  Coverage Ratio: {coverage['coverage_ratio']:.3f}")
print(f"  Dimensions Covered: {coverage['dimensions_covered']}")
print(f"  Dimensions Missing: {coverage['dimensions_missing']}")

print(f"\nConfidence Breakdown:")
print(f"  Avg Evidence Score: {confidence['avg_evidence_score']:.3f}")
print(f"  Avg Retrieval Score: {confidence['avg_retrieval_score']:.3f}")
print(f"  Base Score: {confidence['base_score']:.3f}")
print(f"  Coverage Ratio: {confidence['coverage_ratio']:.3f}")
print(f"  Final Confidence Score: {confidence['confidence_score']:.3f}")

print("\n")
