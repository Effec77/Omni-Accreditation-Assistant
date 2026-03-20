@echo off
echo ========================================
echo Restarting API Server
echo ========================================
echo.
echo Step 1: Stopping any existing API server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *start_api*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Starting fresh API server...
echo.
python api/start_api.py
