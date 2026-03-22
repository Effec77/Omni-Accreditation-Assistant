# Troubleshooting: Full NAAC Audit 404 Error

## Problem
The "Run Full NAAC Audit" button returns a 404 error because the backend needs to be restarted to load the new endpoint.

## Solution

### Step 1: Restart Backend (REQUIRED)

The backend was just restarted by running `FORCE_RESTART_BACKEND.bat`. 

**Wait 15-20 seconds** for it to fully start.

### Step 2: Verify Backend is Running

Open a new terminal and run:
```bash
curl http://127.0.0.1:8000/health
```

You should see: `{"status":"healthy"}`

### Step 3: Verify Full Audit Endpoint Exists

Run:
```bash
curl -X OPTIONS http://127.0.0.1:8000/api/audit/run-full-audit
```

Should return status 200 (not 404).

### Step 4: Hard Refresh Browser

1. Open browser console (F12)
2. Do a HARD refresh:
   - **Windows**: Ctrl + Shift + R or Ctrl + F5
   - **Mac**: Cmd + Shift + R
3. This clears the browser cache

### Step 5: Test Full Audit

1. Make sure your SSR file is uploaded and ingested (green checkmark)
2. Click "Run Full NAAC Audit" button
3. Watch the console for any errors
4. Wait 2-5 minutes for results

## If Still Getting 404

### Option A: Manual Backend Restart

1. Open Task Manager (Ctrl + Shift + Esc)
2. Find all `python.exe` processes
3. End them all
4. Open new terminal:
   ```bash
   cd accreditation_copilot/api
   python start_api.py
   ```
5. Wait for "Uvicorn running on http://127.0.0.1:8000"
6. Hard refresh browser

### Option B: Check Backend Logs

Look at the terminal where backend is running. You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Option C: Test Endpoint Directly

Run this Python script:
```python
import requests

try:
    response = requests.post("http://127.0.0.1:8000/api/audit/run-full-audit")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Endpoint works!")
        result = response.json()
        print(f"CGPA: {result['overall_result']['cgpa']}")
        print(f"Grade: {result['overall_result']['letter_grade']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Connection error: {e}")
```

## Common Issues

### Issue 1: Port 8000 Already in Use
**Solution**: Kill all Python processes and restart

### Issue 2: Python Cache Not Cleared
**Solution**: Delete these folders:
- `accreditation_copilot/api/__pycache__`
- `accreditation_copilot/api/routers/__pycache__`
- `accreditation_copilot/scoring/__pycache__`

### Issue 3: Wrong Working Directory
**Solution**: Make sure you're in the project root when starting backend

### Issue 4: Frontend Cached Old API Calls
**Solution**: Hard refresh browser (Ctrl + Shift + R)

## Verification Checklist

- [ ] Backend is running (check http://127.0.0.1:8000/health)
- [ ] Full audit endpoint exists (OPTIONS request returns 200)
- [ ] Browser cache cleared (hard refresh)
- [ ] SSR file is uploaded and ingested
- [ ] No 404 errors in browser console
- [ ] Backend logs show no errors

## Expected Behavior

When working correctly:
1. Click "Run Full NAAC Audit"
2. See "Analyzing institutional evidence..." spinner
3. Wait 2-5 minutes
4. See Full Audit Dashboard with:
   - Overall CGPA
   - Letter grade (A++, A+, A, etc.)
   - Accreditation status
   - Criterion breakdown
   - Improvement suggestions

## Still Not Working?

If you've tried everything above and it's still not working:

1. Check if `accreditation_copilot/api/routers/audit.py` has the `@router.post("/run-full-audit")` endpoint
2. Verify `accreditation_copilot/scoring/naac_grading.py` exists
3. Make sure all files were saved
4. Try restarting your computer (clears all caches)

## Quick Test Command

Run this to test everything at once:
```bash
# Test backend health
curl http://127.0.0.1:8000/health

# Test full audit endpoint (will fail if no data, but shouldn't 404)
curl -X POST http://127.0.0.1:8000/api/audit/run-full-audit

# Should NOT see "404 Not Found"
# Should see either:
# - 200 OK with JSON result
# - 500 Internal Server Error (if no data ingested)
```

---

**Current Status**: Backend was just restarted. Wait 15-20 seconds, then hard refresh your browser and try again.
