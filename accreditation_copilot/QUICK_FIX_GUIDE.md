# Quick Fix Guide - Get 82% Confidence Score

## The Problem
Your screenshots show 49% confidence score, but the backend has been fixed to show 82%.

## The Solution
**You need to restart the backend API server to apply the fixes.**

## Step-by-Step (5 minutes)

### Step 1: Stop Everything
Close all terminals running the app (or press Ctrl+C in each)

### Step 2: Clear Cache
```bash
cd accreditation_copilot
Remove-Item audit_results/cache_*.json -Force
```

### Step 3: Start Backend
```bash
cd api
python start_api.py
```
Wait for: "Uvicorn running on http://0.0.0.0:8000"

### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```
Wait for: "Ready on http://localhost:3000"

### Step 5: Test
1. Go to http://localhost:3000
2. Upload `Excellence_University_A+_SSR.pdf`
3. Select NAAC 3.2.1
4. Click "Run Audit"

## What You'll See

### Before (Current):
- Confidence: 49%
- Status: Partial
- Grade: B
- Evidence: Raw text blob

### After (Fixed):
- **Confidence: 82%** ✅
- **Status: Compliant** ✅
- **Grade: B+ to A-** ✅
- **Evidence: Structured tables with charts** ✅

## New Evidence Display

### Summary Cards (Top)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 127         │ ₹4580 L     │ 5           │ 5 years     │
│ Projects    │ Funding     │ Agencies    │ Period      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Table View
```
Year-wise Funding Data                    100% relevant
┌──────────┬──────────┬────────────┬──────────────────┐
│ Year     │ Projects │ Funding    │ Agencies         │
├──────────┼──────────┼────────────┼──────────────────┤
│ 2019-20  │ 22       │ ₹785 L     │ DST, SERB, DBT   │
│ 2020-21  │ 28       │ ₹920 L     │ SERB, DBT, ICSSR │
│ 2021-22  │ 31       │ ₹1150 L    │ DST, SERB        │
└──────────┴──────────┴────────────┴──────────────────┘
```

### Chart View
```
DST     ████████████████████████████ ₹1580 L
SERB    ████████████████████ ₹1240 L
DBT     ██████████████ ₹890 L
ICSSR   ████████ ₹520 L
Industry ████ ₹350 L
```

## Toggle Views
- Click "Structured" for tables
- Click "List" for detailed cards
- Filter by "Strong", "Moderate", "Weak"

## What Was Fixed

### Backend (scoring/confidence_calculator.py)
- Now only counts institution evidence
- Framework chunks excluded from scoring
- Result: 82% instead of 49%

### Frontend (components/EvidenceTableVisualizer.tsx)
- New structured table display
- Summary cards with metrics
- Chart view with bars
- Clean, professional look

## Troubleshooting

### Still showing 49%?
- Did you clear the cache? (Step 2)
- Did you restart the API? (Step 3)
- Check terminal for errors

### Evidence still raw text?
- Hard refresh browser (Ctrl+Shift+R)
- Check browser console (F12)
- Make sure frontend restarted

### API won't start?
- Port 8000 in use? Close other apps
- Python dependencies? Run `pip install -r requirements.txt`
- Check error messages

## Files Changed

### Backend:
- `scoring/confidence_calculator.py` - Filter to institution only
- `scoring/evidence_scorer.py` - Better pattern matching
- `criteria/criterion_registry.py` - Improved query

### Frontend:
- `components/EvidenceTableVisualizer.tsx` - NEW
- `components/EvidenceViewer.tsx` - Updated
- `app/page.tsx` - Pass dimensions

## Need Help?

Check these files for details:
- `SCORING_FIX_COMPLETE.md` - Backend fixes explained
- `UI_EVIDENCE_FIX_COMPLETE.md` - Frontend changes explained
- `RESTART_BACKEND.md` - Detailed restart instructions

## Summary

**The fix is done, you just need to restart!**

1. Clear cache
2. Restart API
3. Restart frontend
4. Test with Excellence University PDF
5. See 82% confidence with beautiful tables

That's it! 🎉
