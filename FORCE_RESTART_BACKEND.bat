@echo off
echo ========================================
echo FORCE RESTART - Clearing Cache and Restarting Backend
echo ========================================
echo.

echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul

echo.
echo Step 2: Clearing Python cache...
rmdir /S /Q accreditation_copilot\api\__pycache__ 2>nul
rmdir /S /Q accreditation_copilot\api\routers\__pycache__ 2>nul
rmdir /S /Q accreditation_copilot\scoring\__pycache__ 2>nul

echo.
echo Step 3: Starting fresh backend...
cd accreditation_copilot\api
start "Accreditation Backend - FRESH START" cmd /k "python start_api.py"

echo.
echo ========================================
echo Backend restarted with fresh code!
echo ========================================
echo.
echo IMPORTANT: Wait 15 seconds for backend to fully start
echo.
echo Then:
echo 1. Open browser console (F12)
echo 2. Refresh page (F5 or Ctrl+Shift+R for hard refresh)
echo 3. Click "Run Full NAAC Audit" button
echo 4. Check console for any errors
echo.
pause
