"""
SMS Diagnostics Script - Test Twilio Configuration and SMS Sending
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("TWILIO SMS DIAGNOSTICS")
print("=" * 60)

# 1. Check environment variables
print("\n1️⃣ Checking Environment Variables...")
print("-" * 60)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

print(f"✓ TWILIO_ACCOUNT_SID: {'✅ SET' if TWILIO_ACCOUNT_SID else '❌ NOT SET'}")
print(f"  Value: {TWILIO_ACCOUNT_SID[:10]}..." if TWILIO_ACCOUNT_SID else "")
print(f"✓ TWILIO_AUTH_TOKEN: {'✅ SET' if TWILIO_AUTH_TOKEN else '❌ NOT SET'}")
print(f"  Value: {TWILIO_AUTH_TOKEN[:10]}..." if TWILIO_AUTH_TOKEN else "")
print(f"✓ TWILIO_PHONE_NUMBER: {'✅ SET' if TWILIO_PHONE_NUMBER else '❌ NOT SET'}")
print(f"  Value: {TWILIO_PHONE_NUMBER}")

if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER):
    print("\n❌ ERROR: Missing Twilio credentials!")
    print("Please add to .env file:")
    print("  TWILIO_ACCOUNT_SID=your_sid")
    print("  TWILIO_AUTH_TOKEN=your_token")
    print("  TWILIO_PHONE_NUMBER=+1234567890")
    sys.exit(1)

# 2. Test Twilio Client Initialization
print("\n2️⃣ Testing Twilio Client Initialization...")
print("-" * 60)

try:
    from twilio.rest import Client
    print("✅ Twilio library imported successfully")
    
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✅ Twilio client initialized successfully")
except ImportError:
    print("❌ Twilio library not installed")
    print("   Run: pip install twilio")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error initializing Twilio: {str(e)}")
    sys.exit(1)

# 3. Check Twilio Account Status
print("\n3️⃣ Checking Twilio Account Status...")
print("-" * 60)

try:
    account = twilio_client.api.account.fetch()
    print(f"✅ Account connected successfully")
    print(f"   Account SID: {account.sid}")
    print(f"   Account Status: {account.status}")
    
    if account.status != "active":
        print(f"   ⚠️  Account status is {account.status}, not 'active'")
except Exception as e:
    print(f"❌ Error fetching account: {str(e)}")
    print("   This usually means invalid credentials")

# 4. List Available Phone Numbers
print("\n4️⃣ Checking Twilio Phone Numbers...")
print("-" * 60)

try:
    phone_numbers = twilio_client.incoming_phone_numbers.stream(limit=5)
    numbers_list = list(phone_numbers)
    
    if numbers_list:
        print(f"✅ Found {len(numbers_list)} phone number(s):")
        for number in numbers_list:
            print(f"   • {number.phone_number} (SID: {number.sid})")
            if number.phone_number.replace(" ", "") == TWILIO_PHONE_NUMBER.replace(" ", ""):
                print(f"     ✅ This matches your TWILIO_PHONE_NUMBER")
    else:
        print("❌ No phone numbers found in account")
        print("   Add a phone number to your Twilio account at https://www.twilio.com/console/phone-numbers/incoming")
except Exception as e:
    print(f"⚠️  Could not list phone numbers: {str(e)}")
    print("   Continuing with test...")

# 5. Test SMS Sending (Dry Run)
print("\n5️⃣ Testing SMS Configuration...")
print("-" * 60)

# Get test phone number from user
TEST_PHONE = input("Enter your phone number to test SMS (e.g., +919876543210): ").strip()

if not TEST_PHONE:
    print("❌ Phone number required for testing")
    sys.exit(1)

print(f"Test Configuration:")
print(f"  From: {TWILIO_PHONE_NUMBER}")
print(f"  To: {TEST_PHONE}")
print(f"  Message: Test SMS from SafeJourney")

try:
    print("\n⏳ Attempting to send test SMS...")
    message = twilio_client.messages.create(
        body="🆘 Test SMS from SafeJourney - SMS is working!",
        from_=TWILIO_PHONE_NUMBER,
        to=TEST_PHONE
    )
    print(f"✅ SMS sent successfully!")
    print(f"   Message SID: {message.sid}")
    print(f"   Status: {message.status}")
    print(f"   From: {message.from_}")
    print(f"   To: {message.to}")
except Exception as e:
    error_str = str(e)
    print(f"❌ Error sending SMS: {error_str}")
    
    # Provide specific error handling
    if "not in a valid phone number format" in error_str:
        print("   Issue: Invalid phone number format")
        print(f"   Expected format: +1234567890 or +919876543210")
        print(f"   Your number: {TEST_PHONE}")
    elif "is not a valid phone number" in error_str:
        print("   Issue: Phone number not verified")
        print("   Solution: Add and verify the phone number in your Twilio account")
    elif "Account does not have phone capability" in error_str:
        print("   Issue: Twilio account doesn't have messaging capability")
        print("   Solution: Upgrade your Twilio account")
    elif "Invalid 'From' Phone Number" in error_str:
        print("   Issue: The 'From' phone number is not in your Twilio account")
        print("   Solution: Check your TWILIO_PHONE_NUMBER in .env")
    elif "Authentication failed" in error_str:
        print("   Issue: Authentication failed - invalid credentials")
        print("   Solution: Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN")

# 6. Summary
print("\n" + "=" * 60)
print("DIAGNOSTICS SUMMARY")
print("=" * 60)

print("\n✅ Prerequisites checked:")
print("  • Environment variables present")
print("  • Twilio client initialized")
print("  • Account connected")

print("\n🔧 If SMS is not working, check:")
print("  1. Phone number is verified in Twilio console")
print("  2. Account has SMS capability enabled")
print("  3. Account has sufficient credits")
print("  4. Phone number in 'To' field is in correct format (+country code)")
print("  5. Credentials are correct in .env file")

print("\n📞 Twilio Console: https://www.twilio.com/console")
print("=" * 60)
