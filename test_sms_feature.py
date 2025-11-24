"""
Test script to verify SMS emergency alert feature is working
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_sms"
TEST_PHONE = "+919876543210"  # Change this to your test number

print("=" * 60)
print("SAFE PATH AI - SMS Emergency Alert Feature Test")
print("=" * 60)
print()

# Test 1: Update emergency contact
print("✅ Test 1: Setting emergency contact number...")
try:
    response = requests.post(
        f"{BASE_URL}/api/update-emergency-contact",
        json={
            "uid": TEST_USER_ID,
            "emergency_contact_number": TEST_PHONE
        },
        timeout=5
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Emergency contact updated: {data['emergency_contact_number']}")
        print(f"   ✓ Response: {data['message']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 2: Verify backend SMS configuration
print("✅ Test 2: Checking backend SMS configuration...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"   ✓ Backend is running and healthy")
        print(f"   ✓ Check backend logs for Twilio initialization message")
    else:
        print(f"   ✗ Backend health check failed: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error connecting to backend: {e}")

print()

# Test 3: Create SOS alert (this will trigger SMS send in background)
print("✅ Test 3: Triggering SOS alert (SMS will be sent)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/sos/alert",
        json={
            "user_id": TEST_USER_ID,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "message": "🆘 Test Emergency Alert from SMS Feature Test"
        },
        timeout=5
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ SOS alert created: {data['alert_id']}")
        print(f"   ✓ Message: {data['message']}")
        print(f"   ✓ Nearby users: {data['nearby_users_count']}")
        print(f"   ✓ SMS should be sent to: {TEST_PHONE}")
        print()
        print(f"   💡 Check the backend logs for SMS sending status:")
        print(f"      Look for: '📱 Sending SOS SMS to emergency contacts'")
        print(f"      Success message: '✅ SMS sent to [phone_number]'")
    else:
        print(f"   ✗ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()
print("=" * 60)
print("Test Summary")
print("=" * 60)
print()
print("📱 SMS Feature Components:")
print("   ✓ Backend endpoint: /api/update-emergency-contact")
print("   ✓ Backend endpoint: /api/sos/alert (with SMS sending)")
print("   ✓ Frontend modal: EmergencyContactSetup.jsx")
print("   ✓ SMS service: Twilio (requires configuration)")
print()
print("🚀 Next Steps:")
print("   1. Get Twilio credentials from https://www.twilio.com/try-twilio")
print("   2. Update backend/.env with credentials")
print("   3. Restart backend server")
print("   4. Test SMS delivery to configured phone number")
print()
print("=" * 60)
