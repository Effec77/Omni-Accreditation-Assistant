"""
Deep Score Diagnostic - Find why A+ docs get low scores
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'accreditation_copilot'))

from retrieval.dual_retrieval import DualRetriever
from models.model_manager import get_model_manager
from scoring.evidence_scorer import EvidenceScorer
from scoring.semantic_dimension_checker import SemanticDimensionChecker
from scoring.confidence_calculator import ConfidenceCalculator

print("="*80)
print("DEEP SCORE DIAGNOSTIC - A+ Document Analysis")
print("="*80)

# Initialize
model_manager = get_model_manager()
dual_retriever = DualRetriever(model_manager=model_manager)
evidence_scorer = EvidenceScorer()
dimension_checker = SemanticDimensionChecker()
confidence_calculator = ConfidenceCalculator()

# Test query
test_query = "Details of funding received from government and non-government agencies for research projects"
framework = "NAAC"
criterion = "3.1.1"

print(f"\n[STEP 1] Retrieval for criterion {criterion}")
print(f"Query: {test_query}\n")

retrieval_results, institution_available = dual_retriever.retrieve(
    query=test_query,
    query_variants=[test_query],
    framework=framework,
    query_type='metric',
    top_k_framework=3,
    top_k_institution=7
)

print(f"Retrieved: {len(retrieval_results)} chunks")
print(f"Institution chunks: {sum(1 for r in retrieval_results if r.get('source_type') == 'institution')}")
print(f"Framework chunks: {sum(1 for r in retrieval_results if r.get('source_type') == 'framework')}")

print("\n" + "="*80)
print("[STEP 2] Evidence Scoring Analysis")
print("="*80)

evidence_scores = evidence_scorer.score(retrieval_results)

print("\nInstitution Chunks Evidence Scores:")
for i, (result, score_data) in enumerate(zip(retrieval_results, evidence_scores)):
    if result.get('source_type') == 'institution':
        print(f"\n--- Institution Chunk {i+1} ---")
        print(f"Evidence Score: {score_data['evidence_score']:.3f}")
        print(f"Signals:")
        for signal, value in score_data['signals'].items():
            print(f"  {signal}: {value:.3f}")
        print(f"Reranker Score: {result.get('reranker_score', 0.0):.3f}")
        print(f"Text Preview: {result.get('child_text', '')[:200]}...")

# Calculate average evidence score for institution chunks
inst_scores = [
    evidence_scores[i]['evidence_score'] 
    for i, r in enumerate(retrieval_results) 
    if r.get('source_type') == 'institution'
]
avg_evidence = sum(inst_scores) / len(inst_scores) if inst_scores else 0

print(f"\n>>> Average Institution Evidence Score: {avg_evidence:.3f}")

print("\n" + "="*80)
print("[STEP 3] Dimension Coverage Analysis")
print("="*80)

coverage = dimension_checker.check(retrieval_results, framework, criterion)

print(f"\nCoverage Ratio: {coverage.get('coverage_ratio', 0.0):.3f}")
print(f"Dimensions Covered: {len(coverage.get('dimensions_covered', []))}")
print(f"Dimensions Missing: {len(coverage.get('dimensions_missing', []))}")

if coverage.get('dimensions_missing'):
    print("\nMissing Dimensions:")
    for dim in coverage.get('dimensions_missing', []):
        print(f"  - {dim}")

print("\n" + "="*80)
print("[STEP 4] Confidence Calculation Breakdown")
print("="*80)

confidence = confidence_calculator.calculate(
    evidence_scores,
    coverage,
    retrieval_results
)

print(f"\nBase Score: {confidence.get('base_score', 0.0):.3f}")
print(f"  - Avg Evidence Score: {confidence.get('avg_evidence_score', 0.0):.3f} (weight: 0.6)")
print(f"  - Avg Retrieval Score: {confidence.get('avg_retrieval_score', 0.0):.3f} (weight: 0.4)")
print(f"\nCoverage Ratio: {confidence.get('coverage_ratio', 0.0):.3f}")
print(f"\nFinal Confidence: {confidence.get('confidence_score', 0.0):.3f}")
print(f"  Formula: base_score × coverage_ratio")
print(f"  = {confidence.get('base_score', 0.0):.3f} × {confidence.get('coverage_ratio', 0.0):.3f}")
print(f"  = {confidence.get('confidence_score', 0.0):.3f}")

print("\n" + "="*80)
print("[STEP 5] Problem Identification")
print("="*80)

problems = []

if avg_evidence < 0.5:
    problems.append(f"❌ Low evidence scores (avg: {avg_evidence:.3f})")
    problems.append("   → Institution chunks lack numeric evidence (currency, counts, dates)")
    problems.append("   → Check if documents contain actual data vs templates")

if confidence.get('avg_retrieval_score', 0.0) < 0.5:
    problems.append(f"❌ Low reranker scores (avg: {confidence.get('avg_retrieval_score', 0.0):.3f})")
    problems.append("   → Retrieved chunks not semantically relevant to query")
    problems.append("   → May need better query formulation or more relevant docs")

if coverage.get('coverage_ratio', 0.0) < 1.0:
    problems.append(f"⚠️ Incomplete dimension coverage ({coverage.get('coverage_ratio', 0.0):.1%})")
    problems.append(f"   → Missing {len(coverage.get('dimensions_missing', []))} dimensions")

if not inst_scores:
    problems.append("❌ CRITICAL: No institution chunks retrieved!")
    problems.append("   → System cannot score without institution evidence")

if problems:
    print("\nProblems Found:")
    for problem in problems:
        print(problem)
else:
    print("\n✓ No obvious problems detected")

print("\n" + "="*80)
print("[STEP 6] Recommendations")
print("="*80)

print("\nTo improve scores:")
print("1. Check institution document quality:")
print("   - Should contain actual numbers (funding amounts, project counts)")
print("   - Should have structured data (tables, lists)")
print("   - Should include dates and agency names")
print("")
print("2. Verify document ingestion:")
print("   python check_institution_data.py")
print("")
print("3. Check what's actually in the chunks:")
print("   - Look at the text previews above")
print("   - Are they relevant to the query?")
print("   - Do they contain evidence or just templates?")
print("")
print("4. Consider adjusting scoring weights:")
print("   - Current: 60% evidence quality, 40% retrieval relevance")
print("   - May need to tune for your document types")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
