@echo off
echo ========================================
echo RESTARTING API WITH UPDATED CODE
echo ========================================
echo.

echo Step 1: Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo Cache cleared!
echo.

echo Step 2: Clearing audit cache...
cd /d "%~dp0"
del /q audit_results\cache_*.json 2>nul
echo Audit cache cleared!
echo.

echo Step 3: Starting API server...
echo.
echo IMPORTANT: The API will start now.
echo You should see "Uvicorn running on http://0.0.0.0:8000"
echo.
echo After the API starts:
echo 1. Open a NEW terminal
echo 2. Go to the frontend folder
echo 3. Run: npm run dev
echo.
echo Press any key to start the API...
pause >nul

cd api
python start_api.py
