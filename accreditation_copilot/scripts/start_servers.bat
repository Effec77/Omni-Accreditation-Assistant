@echo off
echo ========================================
echo  Starting Backend and Frontend Servers
echo ========================================
echo.
echo Starting Backend API...
cd /d "%~dp0\.."
start "Backend API" cmd /k "call "%~dp0..\..\venv\Scripts\activate.bat" && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak

echo.
echo Starting Frontend UI...
cd frontend
start "Frontend UI" cmd /k "npm run dev"

echo.
echo ========================================
echo  Both servers are starting!
echo ========================================
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit (servers will keep running)
pause >nul
