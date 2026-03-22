# Backend Restart Instructions

The backend needs to be restarted to load the new `/api/audit/criteria/{framework}` endpoint.

## Steps:

1. **Stop the current backend** (if running):
   - Press `Ctrl+C` in the terminal where the backend is running

2. **Start the backend again**:
   ```bash
   cd accreditation_copilot/api
   python start_api.py
   ```

   OR if you're using uvicorn directly:
   ```bash
   cd accreditation_copilot/api
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify the endpoint works**:
   ```bash
   curl http://127.0.0.1:8000/api/audit/criteria/NAAC
   ```

   You should see a JSON response with 11 NAAC criteria.

## What Changed:

1. **Backend**: Added `GET /api/audit/criteria/{framework}` endpoint to fetch available criteria
2. **Frontend**: 
   - Replaced text input with multi-select dropdown
   - Shows all 11 NAAC criteria and 3 NBA criteria
   - Supports selecting multiple criteria (Hold Ctrl/Cmd)
   - Tracks ingestion status - once ingested, you can test multiple criteria without re-ingesting
3. **Criterion Registry**: Expanded from 5 to 11 NAAC criteria

## Testing:

1. Upload your comprehensive PDF
2. Click "Ingest Files" (only needed once)
3. Select one or multiple criteria from the dropdown
4. Click "Run Audit" - it will run audits for all selected criteria
5. Switch to different criteria and run again - no re-ingestion needed!
