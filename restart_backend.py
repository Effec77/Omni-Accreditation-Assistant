"""
Quick script to restart the backend
"""
import subprocess
import time
import requests
import sys

print("=" * 60)
print("Restarting Backend for Full NAAC Audit")
print("=" * 60)
print()

# Kill existing Python processes running the API
print("Stopping existing backend...")
try:
    subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq *start_api*"], 
                   capture_output=True, timeout=5)
    time.sleep(2)
except:
    pass

print("Starting new backend...")
print()

# Start the backend
try:
    subprocess.Popen(
        ["python", "start_api.py"],
        cwd="accreditation_copilot/api",
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    print("Waiting for backend to start...")
    for i in range(15):
        time.sleep(1)
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=2)
            if response.status_code == 200:
                print(f"\n✅ Backend started successfully!")
                break
        except:
            print(f".", end="", flush=True)
    else:
        print("\n⚠️ Backend may still be starting...")
    
    # Check if the new endpoint exists
    print("\nChecking for /api/audit/run-full-audit endpoint...")
    time.sleep(2)
    try:
        response = requests.options("http://127.0.0.1:8000/api/audit/run-full-audit", timeout=5)
        if response.status_code == 200:
            print("✅ Full audit endpoint is available!")
        else:
            print(f"⚠️ Endpoint returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Endpoint check failed: {e}")
    
    print()
    print("=" * 60)
    print("Backend restart complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Refresh your browser (F5)")
    print("2. Click 'Run Full NAAC Audit' button")
    print()
    
except Exception as e:
    print(f"❌ Error starting backend: {e}")
    sys.exit(1)
