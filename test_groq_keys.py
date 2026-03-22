"""
Test script to verify Groq API keys are loaded correctly
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path("accreditation_copilot/.env")
load_dotenv(env_path)

print("=" * 80)
print("GROQ API KEY VERIFICATION")
print("=" * 80)

# Check for all possible keys
keys_found = []
for i in range(1, 20):  # Check up to KEY_20
    key_name = f"GROQ_API_KEY_{i}"
    key_value = os.getenv(key_name)
    
    if key_value:
        # Mask the key for security (show first 8 and last 4 chars)
        if len(key_value) > 12:
            masked = f"{key_value[:8]}...{key_value[-4:]}"
        else:
            masked = "***"
        
        # Check if it looks valid
        is_valid = key_value.startswith("gsk_") and len(key_value) > 20
        status = "✅ Valid" if is_valid else "❌ Invalid format"
        
        keys_found.append({
            'name': key_name,
            'masked': masked,
            'valid': is_valid
        })
        
        print(f"\n{key_name}:")
        print(f"  Value: {masked}")
        print(f"  Status: {status}")

print(f"\n{'='*80}")
print(f"SUMMARY")
print(f"{'='*80}")
print(f"Total keys found: {len(keys_found)}")
print(f"Valid keys: {sum(1 for k in keys_found if k['valid'])}")
print(f"Invalid keys: {sum(1 for k in keys_found if not k['valid'])}")

if len(keys_found) == 0:
    print("\n❌ NO KEYS FOUND!")
    print("   Make sure .env file exists at: accreditation_copilot/.env")
elif sum(1 for k in keys_found if k['valid']) < len(keys_found):
    print("\n⚠️  SOME KEYS ARE INVALID!")
    print("   Check that all keys start with 'gsk_' and are complete")
else:
    print(f"\n✅ ALL {len(keys_found)} KEYS ARE VALID!")
    print(f"   Total daily token capacity: {len(keys_found) * 100000:,} tokens")
    print(f"   Estimated full audits per day: {(len(keys_found) * 100000) // 70000}")

print(f"\n{'='*80}")
print("NEXT STEPS")
print(f"{'='*80}")

if len(keys_found) < 9:
    print(f"📝 You currently have {len(keys_found)} keys configured.")
    print(f"   Add {9 - len(keys_found)} more keys to reach the target of 9 keys.")
    print(f"   Follow the guide in ADD_GROQ_KEYS_GUIDE.md")
elif len(keys_found) == 9:
    print("✅ Perfect! You have 9 keys configured.")
    print("   Restart the backend to load all keys:")
    print("   1. Run: .\\FORCE_RESTART_BACKEND.bat")
    print("   2. Wait 15 seconds")
    print("   3. Test Full NAAC Audit")
else:
    print(f"✅ Excellent! You have {len(keys_found)} keys configured.")
    print("   This gives you extra capacity for heavy usage.")
    print("   Restart the backend to load all keys.")

print()
