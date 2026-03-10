"""Check evidence scores for Excellence University chunks"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scoring.evidence_scorer import EvidenceScorer
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

print("\n" + "="*80)
print("EVIDENCE SCORING DEBUG")
print("="*80)

for i, (result, score_data) in enumerate(zip(results, evidence_scores), 1):
    source = result.get('source', 'unknown')
    source_type = result.get('source_type', 'unknown')
    reranker = result.get('reranker_score', 0)
    evidence_score = score_data['evidence_score']
    signals = score_data['signals']
    
    # Get text preview (handle unicode)
    text = result.get('child_text', '')[:150].encode('ascii', 'ignore').decode('ascii')
    
    print(f"\n{i}. {source} ({source_type})")
    print(f"   Reranker: {reranker:.3f} | Evidence: {evidence_score:.3f}")
    print(f"   Signals: numeric={signals['numeric']:.2f}, entity={signals['entity']:.2f}, keyword={signals['keyword']:.2f}, structure={signals['structure']:.2f}")
    print(f"   Text: {text}...")

print("\n")
