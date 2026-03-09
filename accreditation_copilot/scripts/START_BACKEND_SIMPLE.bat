@echo off
echo Starting Backend API...
echo.
call "%~dp0..\..\venv\Scripts\activate.bat"
cd /d "%~dp0\.."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
pause
