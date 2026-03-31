"""
Quick test to verify Groq is working (not falling back to Ollama)
"""
import sys
sys.path.insert(0, 'accreditation_copilot')

from utils.llm_fallback import get_llm_fallback_manager

print("=" * 80)
print("TESTING GROQ API (NOT OLLAMA FALLBACK)")
print("=" * 80)

manager = get_llm_fallback_manager()

print("\nMaking test LLM call...")
response, source = manager.completion(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say 'Groq is working!' in one sentence."}],
    max_tokens=50
)

print(f"\n✅ Response from: {source.upper()}")
print(f"Content: {response.choices[0].message.content}")

stats = manager.get_stats()
print(f"\n📊 Statistics:")
print(f"   Total calls: {stats['total_calls']}")
print(f"   Groq calls: {stats['groq_calls']}")
print(f"   Ollama fallbacks: {stats['ollama_fallbacks']}")

if source == 'groq':
    print(f"\n✅ SUCCESS: Using Groq API (not Ollama)")
else:
    print(f"\n❌ ISSUE: Still falling back to Ollama")

print("=" * 80)
