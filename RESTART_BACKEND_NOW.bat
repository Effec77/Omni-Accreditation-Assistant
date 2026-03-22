@echo off
echo ========================================
echo Restarting Backend for Full Audit
echo ========================================
echo.

echo Stopping any existing backend processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *start_api*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend with new endpoints...
cd accreditation_copilot\api
start "Accreditation Backend" cmd /k "python start_api.py"

echo.
echo ========================================
echo Backend restarted!
echo ========================================
echo.
echo The backend should now be running on http://127.0.0.1:8000
echo.
echo Wait 10 seconds for it to fully start, then:
echo 1. Refresh your browser (F5)
echo 2. Click "Run Full NAAC Audit" button
echo.
pause
