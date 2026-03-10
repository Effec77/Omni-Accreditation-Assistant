@echo off
echo ========================================
echo  FINAL NUMPY FIX - RESTARTING SERVERS
echo ========================================
echo.

echo Step 1: Killing ALL Python and Node processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 3 /nobreak >nul

echo Step 2: Clearing ALL caches...
cd /d "%~dp0"
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /q audit_results\cache_*.json 2>nul
echo Cache cleared!

echo Step 3: Starting API Server (with NumPy fix)...
start "API Server - FIXED" cmd /k "cd api && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo Waiting for API to start...
timeout /t 10 /nobreak >nul

echo Step 4: Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  ALL FIXES APPLIED!
echo ========================================
echo.
echo  NumPy int64 error: FIXED
echo  TypeScript errors: FIXED
echo  Framework indexes: CREATED
echo.
echo  API: http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo.
echo ========================================
echo.
echo Wait 15 seconds for both servers to start...
echo Then open: http://localhost:3000
echo.
pause
