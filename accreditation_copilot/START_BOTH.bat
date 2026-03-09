@echo off
echo ========================================
echo  Starting Accreditation Copilot
echo ========================================
echo.
echo Step 1: Starting API Server...
start "API Server" cmd /k "cd api && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul
echo.
echo Step 2: Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo ========================================
echo  Both servers are starting!
echo ========================================
echo  API: http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
pause
