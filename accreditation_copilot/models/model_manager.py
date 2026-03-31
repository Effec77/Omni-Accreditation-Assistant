"""
ModelManager - Centralized model lifecycle management
Loads models once at startup and reuses them across all operations.
"""

import os
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import tiktoken
from groq import Groq
from dotenv import load_dotenv


class ModelManager:
    """
    Singleton manager for all ML models.
    Ensures models are loaded only once and reused across the application.
    """
    
    _instance = None
    _initialized = False
    
    def __init__(self):
        """Private constructor. Use get_instance() instead."""
        if ModelManager._initialized:
            return
        
        # Model storage
        self.embedder = None
        self.reranker_model = None
        self.reranker_tokenizer = None
        self.tokenizer_tiktoken = None
        self.groq_client = None
        self.device = None
        
        # Model names
        self.embedder_name = 'BAAI/bge-base-en-v1.5'
        self.reranker_name = 'BAAI/bge-reranker-base'
        
        ModelManager._initialized = True
    
    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of ModelManager.
        
        Returns:
            ModelManager instance
        """
        if cls._instance is None:
            cls._instance = ModelManager()
            cls._instance.load_models()
        return cls._instance
    
    def load_models(self):
        """Load all models once at startup."""
        print("\n" + "="*80)
        print("MODEL MANAGER: Loading models (one-time initialization)")
        print("="*80)
        
        # Load environment variables
        load_dotenv()
        
        # Authenticate with HuggingFace if token is available
        self._authenticate_huggingface()
        
        # Determine device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        
        # Load embedding model
        print(f"\n[1/5] Loading embedding model: {self.embedder_name}")
        self.embedder = SentenceTransformer(self.embedder_name, device=self.device)
        print(f"[PASS] Embedding model loaded")
        
        # Load reranker model
        print(f"\n[2/5] Loading reranker model: {self.reranker_name}")
        self.reranker_tokenizer = AutoTokenizer.from_pretrained(self.reranker_name)
        self.reranker_model = AutoModelForSequenceClassification.from_pretrained(self.reranker_name)
        self.reranker_model.to(self.device)
        self.reranker_model.eval()
        print(f"[PASS] Reranker model loaded")
        
        # Load tiktoken tokenizer
        print(f"\n[3/5] Loading tiktoken tokenizer")
        self.tokenizer_tiktoken = tiktoken.get_encoding("cl100k_base")
        print(f"[PASS] Tiktoken tokenizer loaded")
        
        # Initialize Groq client (support multiple keys)
        print(f"\n[4/5] Initializing Groq client")
        
        # Try to load multiple Groq API keys
        groq_keys = []
        for i in range(1, 10):  # Support up to 9 keys
            key = os.getenv(f'GROQ_API_KEY_{i}')
            if key:
                groq_keys.append(key)
        
        # Fallback to single GROQ_API_KEY if no numbered keys found
        if not groq_keys:
            single_key = os.getenv('GROQ_API_KEY')
            if single_key:
                groq_keys.append(single_key)
        
        if groq_keys:
            # Use first key for ModelManager (GroqKeyPool handles rotation)
            self.groq_client = Groq(api_key=groq_keys[0])
            print(f"[PASS] Groq client initialized with {len(groq_keys)} key(s) available")
        else:
            print(f"[WARN] No Groq API keys found in environment")
            print(f"[WARN] Set GROQ_API_KEY_1, GROQ_API_KEY_2, etc. in .env file")
            self.groq_client = None
        
        print("\n" + "="*80)
        print("MODEL MANAGER: All models loaded successfully")
        print("="*80 + "\n")
    
    def _authenticate_huggingface(self):
        """Authenticate with HuggingFace Hub if token is available."""
        hf_token = os.getenv('HF_TOKEN')
        
        if hf_token:
            try:
                from huggingface_hub import login
                login(token=hf_token)
                print("[PASS] Authenticated with HuggingFace Hub")
            except Exception as e:
                print(f"[WARN] Failed to authenticate with HuggingFace: {e}")
        else:
            print("[INFO] HF_TOKEN not found - using unauthenticated requests")
    
    def get_embedder(self):
        """Get the embedding model."""
        if self.embedder is None:
            raise RuntimeError("Embedder not loaded. Call load_models() first.")
        return self.embedder
    
    def get_reranker_model(self):
        """Get the reranker model."""
        if self.reranker_model is None:
            raise RuntimeError("Reranker model not loaded. Call load_models() first.")
        return self.reranker_model
    
    def get_reranker_tokenizer(self):
        """Get the reranker tokenizer."""
        if self.reranker_tokenizer is None:
            raise RuntimeError("Reranker tokenizer not loaded. Call load_models() first.")
        return self.reranker_tokenizer
    
    def get_tiktoken_tokenizer(self):
        """Get the tiktoken tokenizer."""
        if self.tokenizer_tiktoken is None:
            raise RuntimeError("Tiktoken tokenizer not loaded. Call load_models() first.")
        return self.tokenizer_tiktoken
    
    def get_groq_client(self):
        """Get the Groq client."""
        if self.groq_client is None:
            raise RuntimeError("Groq client not initialized. Check GROQ_API_KEY in .env")
        return self.groq_client
    
    def get_device(self):
        """Get the compute device (cuda/cpu)."""
        if self.device is None:
            raise RuntimeError("Device not set. Call load_models() first.")
        return self.device
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (for testing purposes only)."""
        cls._instance = None
        cls._initialized = False


# Convenience function for getting the singleton instance
def get_model_manager():
    """Get the ModelManager singleton instance."""
    return ModelManager.get_instance()
