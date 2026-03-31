"""
Test to see what the full audit endpoint is actually returning
"""
import requests
import json

print("=" * 80)
print("TESTING FULL AUDIT RESPONSE")
print("=" * 80)

url = "http://127.0.0.1:8000/api/audit/run-full-audit"

print(f"\nCalling: {url}")
print("This may take 2-5 minutes...\n")

try:
    response = requests.post(url, timeout=300)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ Response received successfully")
        print(f"\nOverall Result:")
        print(json.dumps(result.get('overall_result', {}), indent=2))
        
        print(f"\nSummary:")
        print(json.dumps(result.get('summary', {}), indent=2))
        
        print(f"\nFirst Criterion Sample:")
        if result.get('individual_criteria'):
            print(json.dumps(result['individual_criteria'][0], indent=2))
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "=" * 80)
