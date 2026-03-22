# Quick Reference: LLM Fallback System

## Current Status

✅ **7 Groq API Keys** - 700k tokens/day capacity
✅ **Ollama llama3.1:8b** - Local text generation
✅ **Ollama llava** - Local vision model
✅ **Automatic Fallback** - Enabled and tested

## How to Check System Health

### 1. Check All Groq Keys
```bash
python test_groq_keys.py
```
Expected: All 7 keys show ✅ Valid

### 2. Test Fallback System
```bash
python test_llm_fallback.py
```
Expected: Response from groq or ollama

### 3. Test Full Audit
```bash
python diagnose_audit_issue.py
```
Expected: Audit completes with confidence score

## What Happens When...

### ✅ Groq Has Capacity
```
Request → Groq (fast, cloud) → Response in 1-2 seconds
```

### ⚠️ Groq Rate Limited
```
Request → Groq (rate limit) → Ollama (local) → Response in 5-10 seconds
```

### ❌ Both Fail
```
Request → Groq (fail) → Ollama (fail) → Error message
Action: Check Ollama service (ollama serve)
```

## Common Commands

### Start Ollama Service
```bash
ollama serve
```

### Check Ollama Models
```bash
ollama list
```

### Pull New Ollama Model
```bash
ollama pull llama3.1:8b
ollama pull llava
```

### Restart Backend
```bash
python restart_backend.py
```

## Monitoring Logs

Look for these messages in logs:

### Success with Groq
```
[ComplianceAuditor] Used groq for synthesis
[QueryExpander] Used groq for query expansion
```

### Fallback to Ollama
```
[LLMFallback] Groq rate limit hit, falling back to Ollama...
[ComplianceAuditor] Used ollama for synthesis
```

### Rate Limit Warning
```
Rate limit reached for model `llama-3.3-70b-versatile`
Limit 100000, Used 98700, Requested 1893
```

## Adding More Groq Keys

You mentioned having 7 more accounts (14 more keys). To add them:

1. Edit `accreditation_copilot/.env`
2. Add keys as GROQ_API_KEY_8, GROQ_API_KEY_9, etc.
3. Restart backend: `python restart_backend.py`
4. Verify: `python test_groq_keys.py`

Example:
```bash
GROQ_API_KEY_8=gsk_your_key_here
GROQ_API_KEY_9=gsk_your_key_here
```

## Troubleshooting

### Problem: "Ollama not available"
**Solution**: Start Ollama service
```bash
ollama serve
```

### Problem: "Model not found"
**Solution**: Pull the model
```bash
ollama pull llama3.1:8b
```

### Problem: "All keys rate limited"
**Solution**: 
1. Wait for rate limit reset (shown in error message)
2. Or add more Groq keys
3. System will use Ollama automatically

### Problem: "Low confidence scores"
**Solution**: This is a data issue, not LLM issue
- Upload more institutional documents
- Check institution data: `python check_institution_data.py`

## Performance Comparison

| Backend | Speed | Cost | Capacity |
|---------|-------|------|----------|
| Groq | 1-2s | Free tier | 700k tokens/day (7 keys) |
| Ollama | 5-10s | Free | Unlimited (local) |

## Statistics

Check usage stats:
```python
from utils.llm_fallback import get_llm_fallback_manager

manager = get_llm_fallback_manager()
stats = manager.get_stats()

print(f"Groq success rate: {stats['groq_success_rate']:.1f}%")
print(f"Ollama fallback rate: {stats['ollama_fallback_rate']:.1f}%")
```

## Quick Fixes

### Backend not responding
```bash
python restart_backend.py
```

### Ollama not working
```bash
# Check if running
ollama list

# If not, start it
ollama serve
```

### Need more capacity
```bash
# Add more Groq keys to .env
# Then restart
python restart_backend.py
```

---

**Last Updated**: 2026-03-23
**System Status**: ✅ Operational
