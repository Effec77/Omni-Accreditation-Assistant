import re

# Test the currency pattern
CURRENCY_PATTERN = re.compile(r'(rs\.?|inr|₹)?\s*\d+(\.\d+)?\s*(crore|lakh|lakhs|million)', re.IGNORECASE)

test_texts = [
    "Funding: 1240 Lakhs",
    "INR 1240 Lakhs",
    "Rs. 1240 Lakhs",
    "₹1240 Lakhs",
    "Total: 4580 lakhs",
    "Amount: 85 Lakhs"
]

print("Testing CURRENCY_PATTERN:")
for text in test_texts:
    matches = CURRENCY_PATTERN.findall(text)
    print(f"  '{text}' -> {len(matches)} matches: {matches}")
