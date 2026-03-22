# Adding Additional Groq API Keys

## Current Status
- You have 3 Groq API keys configured (KEY_1, KEY_2, KEY_3)
- KEY_1 has hit its daily rate limit (100,000 tokens used)
- You want to add 6 more keys from 3 additional accounts

## Step-by-Step Instructions

### Step 1: Generate API Keys from Your Accounts

For each of your 3 additional Groq accounts:

1. Go to https://console.groq.com/
2. Log in with account credentials
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Name it (e.g., "Accreditation Copilot Key 1")
6. Copy the key (starts with `gsk_`)
7. Repeat to create a second key for the same account

You should end up with:
- Account 2: 2 keys
- Account 3: 2 keys  
- Account 4: 2 keys
- **Total: 6 new keys**

### Step 2: Add Keys to .env File

Open `accreditation_copilot/.env` and replace the placeholder keys:

```env
# Groq API Keys (Multi-key pool for load balancing)
GROQ_API_KEY_1=gsk_PASTE_YOUR_ACCOUNT_1_KEY_1_HERE
GROQ_API_KEY_2=gsk_PASTE_YOUR_ACCOUNT_1_KEY_2_HERE
GROQ_API_KEY_3=gsk_PASTE_YOUR_ACCOUNT_1_KEY_3_HERE
GROQ_API_KEY_4=gsk_PASTE_YOUR_ACCOUNT_2_KEY_1_HERE
GROQ_API_KEY_5=gsk_PASTE_YOUR_ACCOUNT_2_KEY_2_HERE
GROQ_API_KEY_6=gsk_PASTE_YOUR_ACCOUNT_3_KEY_1_HERE
GROQ_API_KEY_7=gsk_PASTE_YOUR_ACCOUNT_3_KEY_2_HERE
GROQ_API_KEY_8=gsk_PASTE_YOUR_ACCOUNT_4_KEY_1_HERE
GROQ_API_KEY_9=gsk_PASTE_YOUR_ACCOUNT_4_KEY_2_HERE
```

**IMPORTANT**: Make sure each key starts with `gsk_` and has no extra spaces or quotes.

### Step 3: Restart Backend

After adding the keys, restart the backend to load them:

```bash
# Option A: Use the force restart script
.\FORCE_RESTART_BACKEND.bat

# Option B: Manual restart
# 1. Kill all Python processes (Ctrl+C in backend terminal)
# 2. cd accreditation_copilot/api
# 3. python start_api.py
```

### Step 4: Verify Keys Are Loaded

Run this test script:

```bash
python test_groq_keys.py
```

You should see:
```
✅ Loaded 9 Groq API keys
Key 1: gsk_OI8E... (Active)
Key 2: gsk_rjGE... (Active)
Key 3: gsk_eLG8... (Active)
Key 4: gsk_XXXX... (Active)
...
```

### Step 5: Test Full Audit

1. Refresh browser (Ctrl + Shift + R)
2. Click "Run Full NAAC Audit"
3. System will automatically rotate through all 9 keys
4. Should complete successfully with proper CGPA scores

## How Key Rotation Works

The system uses a **round-robin key pool**:

1. Starts with KEY_1
2. If KEY_1 hits rate limit → switches to KEY_2
3. If KEY_2 hits rate limit → switches to KEY_3
4. And so on through all 9 keys
5. Each key has 100,000 tokens/day limit
6. With 9 keys = 900,000 tokens/day total capacity

## Token Usage Estimates

For Full NAAC Audit (11 criteria):
- Per criterion: ~5,000-8,000 tokens
- Total per audit: ~55,000-88,000 tokens
- With 9 keys: Can run ~10-16 full audits per day

## Troubleshooting

### Issue: "All API keys exhausted"
**Solution**: Wait for rate limits to reset (resets at midnight UTC) or add more keys

### Issue: "Invalid API key"
**Solution**: Double-check the key format (should start with `gsk_`) and ensure no typos

### Issue: Keys not loading
**Solution**: 
1. Check .env file has no syntax errors
2. Restart backend completely
3. Check backend logs for "Groq client initialized with X key(s)"

### Issue: Still getting 0 scores
**Solution**:
1. Verify keys are loaded: Check backend startup logs
2. Test a single criterion first (not full audit)
3. Check backend logs for rate limit errors

## Testing Individual Keys

To test if a specific key works:

```python
import os
from groq import Groq

# Test KEY_4
os.environ['GROQ_API_KEY'] = 'gsk_YOUR_KEY_HERE'
client = Groq()

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print("✅ Key works!")
except Exception as e:
    print(f"❌ Key failed: {e}")
```

## Expected Behavior After Adding Keys

1. **Backend startup**: Should show "Groq client initialized with 9 key(s)"
2. **Full audit**: Should complete without rate limit errors
3. **Scores**: Should show realistic CGPA (not 0)
4. **Key rotation**: Backend logs will show "Switching to next API key" when rotating

## Quick Verification Checklist

- [ ] Generated 6 new API keys from 3 accounts
- [ ] Added all 6 keys to .env file (KEY_4 through KEY_9)
- [ ] Verified no typos or extra spaces in keys
- [ ] Restarted backend
- [ ] Checked backend logs show "9 key(s) available"
- [ ] Tested full audit
- [ ] Received non-zero CGPA scores

---

**Once you've added the keys and restarted, the Full NAAC Audit should work perfectly with realistic scores!**
