# How to Run the Accreditation Copilot

## ✅ All Errors Fixed!

All TypeScript errors have been fixed and framework indexes have been created.

## Quick Start

### Option 1: Use Batch Files (Windows)

1. **Double-click** `START_BOTH.bat` in the `accreditation_copilot` folder
   - This will open two command windows (API and Frontend)
   - Wait for both to finish loading

### Option 2: Manual Start (Recommended for troubleshooting)

**Terminal 1 - API Server:**
```bash
cd accreditation_copilot/api
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Wait for: `Application startup complete`

**Terminal 2 - Frontend:**
```bash
cd accreditation_copilot/frontend
npm run dev
```

Wait for: `Ready on http://localhost:3000`

## Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Test the System

1. Go to http://localhost:3000
2. Upload `Excellence_University_A+_SSR.pdf` (from `data/raw_docs/`)
3. Select framework: **NAAC**
4. Select metric: **3.2.1**
5. Click **"Run Audit"**

### Expected Results:
- **Confidence Score**: ~77% (High/Compliant)
- **Grade**: B+ to A-
- **Evidence**: Structured tables with funding data
- **Summary Cards**: Total Projects, Total Funding, Agencies, Time Period

## Troubleshooting

### Port 8000 Already in Use

```bash
# Windows PowerShell:
Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }

# Then restart the API server
```

### Frontend Won't Start

```bash
cd frontend
npm install
npm run dev
```

### API Won't Start

```bash
cd api
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Still Showing 49% Confidence?

The backend code is fixed. If you still see 49%:
1. Make sure you killed ALL Python processes
2. Restart the API server
3. Hard refresh the browser (Ctrl+Shift+R)

### Tables Still Empty?

1. Hard refresh browser (Ctrl+Shift+R)
2. Clear browser cache
3. Check browser console (F12) for errors

## What Was Fixed

### 1. TypeScript Errors
- Fixed Set iteration issues in `EvidenceTableVisualizer.tsx`
- Added proper type annotations in `EvidenceViewer.tsx`
- All components now compile without errors

### 2. Missing Framework Indexes
- Created empty framework indexes (NAAC/NBA)
- System now works without framework PDFs
- To add framework data later, place PDFs in:
  - `data/raw_docs/naac/`
  - `data/raw_docs/nba/`
  - Then run: `python ingestion/run_ingestion.py`

### 3. Backend Scoring
- Confidence calculator filters to institution chunks only
- Better pattern matching for currency and projects
- Improved query templates for better retrieval

### 4. Evidence Display
- Complete rewrite of table visualizer
- Flexible pattern matching for multiple formats
- Professional styling with summary cards
- Chart view with gradient bars

## Files Created/Modified

### New Files:
- `START_API.bat` - Start API server
- `START_BOTH.bat` - Start both servers
- `create_minimal_framework_indexes.py` - Create empty framework indexes
- `HOW_TO_RUN.md` - This file

### Modified Files:
- `frontend/components/EvidenceTableVisualizer.tsx` - Fixed TypeScript errors
- `frontend/components/EvidenceViewer.tsx` - Fixed TypeScript errors
- `api/start_api.py` - Fixed Unicode encoding issue

## Notes

- The system currently has empty framework indexes
- This means it won't have NAAC/NBA guidelines for comparison
- But it will work for analyzing institution documents
- The confidence scores and evidence display will work correctly

## Need Help?

Check these files for more details:
- `FINAL_FIX_SUMMARY.md` - Complete fix explanation
- `QUICK_START.txt` - Quick reference
- `SCORING_FIX_COMPLETE.md` - Backend changes
- `UI_EVIDENCE_FIX_COMPLETE.md` - Frontend changes
