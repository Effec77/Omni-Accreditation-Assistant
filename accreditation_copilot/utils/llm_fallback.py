"""
LLM Fallback System
Automatically falls back to Ollama when Groq rate limits are hit.
Supports both text generation (llama3.1:8b) and vision (llava).
"""

import os
import requests
from typing import List, Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMFallbackManager:
    """
    Manages LLM calls with automatic fallback from Groq to Ollama.
    
    Priority:
    1. Groq API (fast, cloud-based)
    2. Ollama llama3.1:8b (local fallback for text)
    3. Ollama llava (local fallback for vision tasks)
    """
    
    def __init__(self):
        """Initialize fallback manager with Groq pool and Ollama config."""
        from utils.groq_pool import GroqKeyPool
        
        # Initialize Groq pool
        try:
            self.groq_pool = GroqKeyPool()
            self.groq_available = True
            print(f"[LLMFallback] Groq pool initialized with {self.groq_pool.get_key_count()} keys")
        except Exception as e:
            print(f"[LLMFallback] Groq initialization failed: {e}")
            self.groq_pool = None
            self.groq_available = False
        
        # Ollama configuration
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_text_model = "llama3.1:8b"
        self.ollama_vision_model = "llava"
        
        # Check Ollama availability
        self.ollama_available = self._check_ollama()
        
        # Statistics
        self.stats = {
            'groq_calls': 0,
            'groq_failures': 0,
            'ollama_fallbacks': 0,
            'total_calls': 0
        }
    
    def _check_ollama(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                
                has_llama = any('llama3.1:8b' in name for name in model_names)
                has_llava = any('llava' in name for name in model_names)
                
                print(f"[LLMFallback] Ollama available - llama3.1:8b: {has_llama}, llava: {has_llava}")
                return has_llama or has_llava
            return False
        except Exception as e:
            print(f"[LLMFallback] Ollama not available: {e}")
            return False
    
    def completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> tuple[Any, str]:
        """
        Create a chat completion with automatic fallback.
        
        Args:
            model: Model name (Groq model name)
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments
            
        Returns:
            Tuple of (response, source) where source is 'groq' or 'ollama'
        """
        self.stats['total_calls'] += 1
        
        # Try Groq first
        if self.groq_available and self.groq_pool:
            try:
                response, key_index = self.groq_pool.completion(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                self.stats['groq_calls'] += 1
                return response, 'groq'
                
            except Exception as e:
                error_str = str(e)
                self.stats['groq_failures'] += 1
                
                # Check if it's a rate limit error
                if 'rate_limit' in error_str.lower() or '429' in error_str:
                    print(f"[LLMFallback] Groq rate limit hit, falling back to Ollama...")
                else:
                    print(f"[LLMFallback] Groq error: {error_str[:100]}, falling back to Ollama...")
        
        # Fallback to Ollama
        if self.ollama_available:
            try:
                response = self._ollama_completion(messages, temperature, max_tokens)
                self.stats['ollama_fallbacks'] += 1
                return response, 'ollama'
            except Exception as e:
                print(f"[LLMFallback] Ollama fallback failed: {e}")
                raise Exception(f"Both Groq and Ollama failed. Last error: {e}")
        else:
            raise Exception("Groq failed and Ollama is not available")
    
    def _ollama_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Any:
        """
        Call Ollama API for completion.
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Response object compatible with Groq format
        """
        # Convert messages to Ollama format (simple prompt)
        prompt = self._messages_to_prompt(messages)
        
        # Call Ollama generate API
        response = requests.post(
            f"{self.ollama_host}/api/generate",
            json={
                "model": self.ollama_text_model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code}")
        
        result = response.json()
        
        # Convert to Groq-compatible format
        class OllamaResponse:
            def __init__(self, text):
                self.choices = [type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': text
                    })()
                })()]
        
        return OllamaResponse(result.get('response', ''))
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt string."""
        prompt_parts = []
        
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            **self.stats,
            'groq_success_rate': (
                (self.stats['groq_calls'] / self.stats['total_calls'] * 100)
                if self.stats['total_calls'] > 0 else 0
            ),
            'ollama_fallback_rate': (
                (self.stats['ollama_fallbacks'] / self.stats['total_calls'] * 100)
                if self.stats['total_calls'] > 0 else 0
            )
        }
    
    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            'groq_calls': 0,
            'groq_failures': 0,
            'ollama_fallbacks': 0,
            'total_calls': 0
        }


# Singleton instance
_fallback_manager = None


def get_llm_fallback_manager() -> LLMFallbackManager:
    """Get singleton instance of LLMFallbackManager."""
    global _fallback_manager
    if _fallback_manager is None:
        _fallback_manager = LLMFallbackManager()
    return _fallback_manager


# Example usage
if __name__ == "__main__":
    manager = get_llm_fallback_manager()
    
    print("\nTesting LLM Fallback System...")
    
    # Test completion
    try:
        response, source = manager.completion(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'Hello from fallback system' in one sentence."}
            ],
            max_tokens=50
        )
        
        print(f"\nResponse from {source}:")
        print(response.choices[0].message.content)
        
        print("\nStatistics:")
        stats = manager.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"\nError: {e}")
