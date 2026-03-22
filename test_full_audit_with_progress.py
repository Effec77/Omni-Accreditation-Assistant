"""
Test full audit with progress tracking
"""
import requests
import time

print("=" * 80)
print("TESTING FULL NAAC AUDIT WITH NEW API KEYS")
print("=" * 80)

url = "http://127.0.0.1:8000/api/audit/run-full-audit"

print(f"\nSending POST to: {url}")
print("This will take 2-5 minutes to evaluate all 11 criteria...")
print("\nProgress:")

start_time = time.time()

try:
    # Increase timeout to 10 minutes
    response = requests.post(url, timeout=600)
    
    elapsed = time.time() - start_time
    print(f"\n✅ Completed in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "=" * 80)
        print("FULL AUDIT RESULTS")
        print("=" * 80)
        
        overall = result.get('overall_result', {})
        summary = result.get('summary', {})
        
        print(f"\n📊 OVERALL NAAC GRADE:")
        print(f"   CGPA: {overall.get('cgpa', 'N/A')} / 4.00")
        print(f"   Letter Grade: {overall.get('letter_grade', 'N/A')}")
        print(f"   Description: {overall.get('description', 'N/A')}")
        print(f"   Accreditation Status: {overall.get('accreditation_status', 'N/A')}")
        
        print(f"\n📈 SUMMARY:")
        print(f"   Criteria Evaluated: {summary.get('criteria_evaluated', 0)}")
        print(f"   Metrics Evaluated: {summary.get('metrics_evaluated', 0)}")
        
        # Show breakdown
        breakdown = overall.get('breakdown', [])
        if breakdown:
            print(f"\n📋 CRITERION BREAKDOWN:")
            for criterion in breakdown:
                print(f"   {criterion.get('criterion', 'N/A')}: {criterion.get('grade', 'N/A')} "
                      f"(GP: {criterion.get('average_grade_points', 0):.2f}, "
                      f"Weight: {criterion.get('weight', 0)} pts)")
        
        # Check if scores are realistic
        cgpa = overall.get('cgpa', 0)
        if cgpa == 0:
            print(f"\n❌ ISSUE: CGPA is still 0!")
            print("   This means the API keys may still be rate limited.")
            print("   Check backend logs for rate limit errors.")
        elif cgpa < 1.0:
            print(f"\n⚠️  WARNING: CGPA is very low ({cgpa})")
            print("   This may indicate scoring issues or poor document quality.")
        else:
            print(f"\n✅ SUCCESS: CGPA is realistic ({cgpa})")
            print("   The Full NAAC Audit is working correctly!")
        
    else:
        print(f"\n❌ Error: Status {response.status_code}")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print(f"\n⏱️ TIMEOUT after {time.time() - start_time:.1f} seconds")
    print("   The audit is taking longer than expected.")
    print("   This is normal for the first run. Check the browser UI for results.")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 80)
