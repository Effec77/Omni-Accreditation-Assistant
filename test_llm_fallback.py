"""
Test LLM Fallback System
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'accreditation_copilot'))

from utils.llm_fallback import get_llm_fallback_manager

print("="*80)
print("LLM FALLBACK SYSTEM TEST")
print("="*80)

# Get manager
manager = get_llm_fallback_manager()

print("\n[1/2] Testing completion with fallback...")

try:
    response, source = manager.completion(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Explain NAAC accreditation in one sentence."}
        ],
        max_tokens=100
    )
    
    print(f"\n✓ Response received from: {source}")
    print(f"Content: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n[2/2] Checking statistics...")
stats = manager.get_stats()

print("\nUsage Statistics:")
print(f"  Total calls: {stats['total_calls']}")
print(f"  Groq calls: {stats['groq_calls']}")
print(f"  Groq failures: {stats['groq_failures']}")
print(f"  Ollama fallbacks: {stats['ollama_fallbacks']}")
print(f"  Groq success rate: {stats['groq_success_rate']:.1f}%")
print(f"  Ollama fallback rate: {stats['ollama_fallback_rate']:.1f}%")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
