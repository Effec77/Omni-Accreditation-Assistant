# Restart Backend to Apply Fixes

The backend scoring fixes have been applied, but you need to restart the API server to see the changes.

## Steps to Restart

### 1. Stop the Current API Server

If the API server is running, stop it:
- Press `Ctrl+C` in the terminal where it's running
- Or close the terminal window

### 2. Clear the Audit Cache

```bash
cd accreditation_copilot
Remove-Item audit_results/cache_*.json -Force
```

### 3. Start the API Server

```bash
cd api
python start_api.py
```

Wait for the message: "Uvicorn running on http://0.0.0.0:8000"

### 4. Restart the Frontend (if needed)

```bash
cd frontend
npm run dev
```

### 5. Test the Fix

1. Go to http://localhost:3000
2. Upload `Excellence_University_A+_SSR.pdf`
3. Select NAAC framework and criterion 3.2.1
4. Click "Run Audit"

**Expected Results:**
- Confidence Score: ~82% (was 49%)
- Compliance Status: Compliant (was Partial)
- Grade: B+ to A- (was B)
- Evidence displayed as structured tables with summary cards

## What Was Fixed

1. **Query Template** - More specific keywords (DST, SERB, DBT, ICSSR, Lakhs)
2. **Evidence Patterns** - Better detection of table-formatted data
3. **Scoring Logic** - Only institution chunks count (framework chunks excluded)
4. **Evidence Display** - New structured table view with charts

## Troubleshooting

### If score is still 49%:
- Make sure you cleared the cache (step 2)
- Verify the API server restarted successfully
- Check the terminal for any errors

### If evidence is still raw text:
- Hard refresh the browser (Ctrl+Shift+R)
- Clear browser cache
- Check browser console for errors (F12)

### If API won't start:
- Check if port 8000 is already in use
- Make sure all Python dependencies are installed
- Check for error messages in the terminal
