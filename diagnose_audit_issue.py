"""
Diagnose why audits are returning 0 scores
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'accreditation_copilot'))

from retrieval.dual_retrieval import DualRetriever
from models.model_manager import get_model_manager
from scoring.scoring_pipeline import ScoringPipeline

print("="*80)
print("AUDIT DIAGNOSTIC TEST")
print("="*80)

# Initialize components
print("\n[1/4] Initializing components...")
model_manager = get_model_manager()
dual_retriever = DualRetriever(model_manager=model_manager)
scoring_pipeline = ScoringPipeline()

# Test query for a simple criterion
test_query = "Details of funding received from government and non-government agencies for research projects"
framework = "NAAC"
criterion = "3.1.1"

print(f"\n[2/4] Testing retrieval for criterion {criterion}...")
print(f"Query: {test_query}")

# Run retrieval
retrieval_results, institution_evidence_available = dual_retriever.retrieve(
    query=test_query,
    query_variants=[test_query],
    framework=framework,
    query_type='metric',
    top_k_framework=3,
    top_k_institution=7
)

print(f"\n[3/4] Retrieval Results:")
print(f"  Total chunks retrieved: {len(retrieval_results)}")
print(f"  Institution evidence available: {institution_evidence_available}")

# Count by source type
framework_count = sum(1 for r in retrieval_results if r.get('source_type') == 'framework')
institution_count = sum(1 for r in retrieval_results if r.get('source_type') == 'institution')

print(f"  Framework chunks: {framework_count}")
print(f"  Institution chunks: {institution_count}")

if institution_count == 0:
    print("\n⚠️ PROBLEM FOUND: No institution chunks retrieved!")
    print("This is why confidence score is 0.")
    print("\nPossible causes:")
    print("1. Institution documents don't contain relevant content for this query")
    print("2. Embedding similarity is too low")
    print("3. Institution index is not properly built")
else:
    print("\n✓ Institution chunks found, proceeding to scoring...")
    
    # Run scoring
    print(f"\n[4/4] Running scoring pipeline...")
    compliance_report = scoring_pipeline.process(
        query=test_query,
        framework=framework,
        criterion=criterion,
        retrieval_results=retrieval_results
    )
    
    confidence_score = compliance_report.get('confidence_score', 
                                            compliance_report.get('confidence', {}).get('overall_confidence', 0.0))
    coverage_ratio = compliance_report.get('coverage_ratio',
                                          compliance_report.get('coverage', {}).get('coverage_ratio', 0.0))
    
    print(f"\nScoring Results:")
    print(f"  Confidence Score: {confidence_score:.3f}")
    print(f"  Coverage Ratio: {coverage_ratio:.3f}")
    
    if confidence_score == 0.0:
        print("\n⚠️ PROBLEM: Confidence score is still 0!")
        print("Checking evidence scores...")
        
        # Check evidence scores
        from scoring.evidence_scorer import EvidenceScorer
        evidence_scorer = EvidenceScorer()
        evidence_scores = evidence_scorer.score(retrieval_results)
        
        print("\nEvidence Scores:")
        for i, score_data in enumerate(evidence_scores[:5]):
            result = retrieval_results[i]
            print(f"\n  Chunk {i+1}:")
            print(f"    Source Type: {result.get('source_type')}")
            print(f"    Evidence Score: {score_data['evidence_score']:.3f}")
            print(f"    Signals: {score_data['signals']}")
            print(f"    Text preview: {result.get('child_text', '')[:100]}...")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
