"""
Simple test for full audit endpoint
"""
import requests

print("Testing Full NAAC Audit Endpoint...")
print("=" * 60)

url = "http://127.0.0.1:8000/api/audit/run-full-audit"

try:
    print(f"\nSending POST to: {url}")
    response = requests.post(url, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 404:
        print("\n❌ 404 NOT FOUND - Endpoint does not exist")
        print("The backend needs to be restarted to load the new endpoint.")
    elif response.status_code == 500:
        print("\n⚠️ 500 INTERNAL SERVER ERROR")
        print("Endpoint exists but failed (probably no data ingested)")
        print("Error:", response.text[:200])
    elif response.status_code == 200:
        print("\n✅ SUCCESS! Endpoint works!")
        result = response.json()
        print(f"CGPA: {result['overall_result']['cgpa']}")
        print(f"Grade: {result['overall_result']['letter_grade']}")
    else:
        print(f"\n⚠️ Unexpected status: {response.status_code}")
        print(response.text[:200])
        
except requests.exceptions.ConnectionError:
    print("\n❌ CONNECTION ERROR - Backend is not running")
    print("Start backend with: cd accreditation_copilot/api && python start_api.py")
except requests.exceptions.Timeout:
    print("\n⏱️ TIMEOUT - Request took too long")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 60)
