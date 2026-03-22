"""
Test script for Full NAAC Audit endpoint
"""
import requests
import json

def test_full_audit():
    """Test the full NAAC audit endpoint"""
    
    print("Testing Full NAAC Audit Endpoint...")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/api/audit/run-full-audit"
    
    try:
        print(f"\nSending POST request to: {url}")
        response = requests.post(url, timeout=300)  # 5 minute timeout
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Full Audit Successful!")
            print("=" * 60)
            
            # Overall result
            overall = result.get('overall_result', {})
            print(f"\n📊 OVERALL NAAC GRADE:")
            print(f"   CGPA: {overall.get('cgpa', 'N/A')}")
            print(f"   Letter Grade: {overall.get('letter_grade', 'N/A')}")
            print(f"   Description: {overall.get('description', 'N/A')}")
            print(f"   Accreditation Status: {overall.get('accreditation_status', 'N/A')}")
            
            # Summary
            summary = result.get('summary', {})
            print(f"\n📈 SUMMARY:")
            print(f"   Criteria Evaluated: {summary.get('criteria_evaluated', 0)}")
            print(f"   Metrics Evaluated: {summary.get('metrics_evaluated', 0)}")
            print(f"   Framework: {summary.get('framework', 'N/A')}")
            
            # Breakdown
            breakdown = overall.get('breakdown', [])
            print(f"\n📋 CRITERION BREAKDOWN ({len(breakdown)} criteria):")
            for criterion in breakdown:
                print(f"   {criterion.get('criterion', 'N/A')}: {criterion.get('grade', 'N/A')} "
                      f"(Weight: {criterion.get('weight', 0)} points, "
                      f"Avg GP: {criterion.get('average_grade_points', 0):.2f})")
            
            # Improvement suggestions
            suggestions = result.get('improvement_suggestions', [])
            if suggestions:
                print(f"\n💡 IMPROVEMENT SUGGESTIONS ({len(suggestions)}):")
                for i, suggestion in enumerate(suggestions[:3], 1):
                    print(f"   {i}. {suggestion[:100]}...")
            
            # Save full result to file
            with open('full_audit_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Full result saved to: full_audit_result.json")
            
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️ Request timed out (took longer than 5 minutes)")
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error - is the backend running?")
        print("   Start backend with: cd accreditation_copilot/api && python start_api.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_full_audit()
