"""
Quick test script for chatbot endpoint
"""
import requests
import json

def test_chatbot():
    url = "http://localhost:8000/api/chatbot/chat"
    
    payload = {
        "message": "How do I get started?",
        "history": []
    }
    
    print("Testing chatbot endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nSending request...")
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"\nBot Response:")
            print(f"{data['response']}")
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR")
        print("API server is not running on port 8000")
        print("\nTo start the server:")
        print("  1. cd accreditation_copilot")
        print("  2. start_api_simple.bat")
        
    except requests.exceptions.Timeout:
        print("\n⏱️ TIMEOUT")
        print("Request took too long (>15 seconds)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_chatbot()
