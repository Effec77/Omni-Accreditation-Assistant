@echo off
echo ========================================
echo  QUICK FIX AND RUN
echo ========================================
echo.

echo Step 1: Killing any existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /q audit_results\cache_*.json 2>nul

echo Step 3: Starting API Server...
start "API Server" cmd /k "cd api && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 8 /nobreak >nul

echo Step 4: Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  SERVERS STARTING!
echo ========================================
echo  API: http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Wait 10 seconds then open: http://localhost:3000
echo.
pause
