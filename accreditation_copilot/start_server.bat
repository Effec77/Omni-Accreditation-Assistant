@echo off
cd /d "D:\GitHub\MultiModal Project"
call "venv\Scripts\activate.bat"
cd accreditation_copilot\api
python -m uvicorn main:app --host 0.0.0.0 --port 8000
