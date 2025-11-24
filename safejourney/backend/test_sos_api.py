"""
Direct API Test - Test SOS SMS with specific phone number
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_sos_with_phone():
    """Test complete SOS flow with user-provided phone number"""
    
    print("=" * 70)
    print("DIRECT API TEST: SOS SMS Feature")
    print("=" * 70)
    
    # Step 1: Get phone number from user
    print("\n1️⃣ ENTER YOUR PHONE NUMBER")
    print("-" * 70)
    phone = input("Enter your phone number (with country code, e.g., +919876543210): ").strip()
    
    if not phone:
        print("❌ Phone number required")
        return False
    
    user_id = "test_user_" + str(datetime.now().timestamp()).replace(".", "")
    
    # Step 2: Update emergency contact
    print("\n2️⃣ UPDATING EMERGENCY CONTACT IN DATABASE")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/update-emergency-contact",
            json={
                "uid": user_id,
                "emergency_contact_number": phone
            }
        )
        
        if response.ok:
            data = response.json()
            print(f"✅ Emergency contact updated!")
            print(f"   UID: {data.get('uid')}")
            print(f"   Saved number: {data.get('emergency_contact_number')}")
        else:
            print(f"❌ Failed to update: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 3: Verify emergency contact was saved
    print("\n3️⃣ VERIFYING EMERGENCY CONTACT IN DATABASE")
    print("-" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/check-emergency-contact?uid={user_id}")
        
        if response.ok:
            data = response.json()
            has_contact = data.get('has_emergency_contact', False)
            saved_number = data.get('emergency_contact_number', 'Not set')
            
            print(f"✅ Database check completed!")
            print(f"   Has emergency contact: {has_contact}")
            print(f"   Saved number: {saved_number}")
            
            if not has_contact:
                print(f"⚠️  Emergency contact not found in database!")
                return False
        else:
            print(f"❌ Failed to check: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 4: Trigger SOS alert
    print("\n4️⃣ TRIGGERING SOS ALERT")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/sos/alert",
            json={
                "user_id": user_id,
                "latitude": 17.38,
                "longitude": 78.38,
                "message": "🆘 TEST SOS ALERT - SMS should go to: " + phone
            }
        )
        
        if response.ok:
            data = response.json()
            print(f"✅ SOS alert triggered!")
            print(f"   Alert ID: {data.get('alert_id')}")
            print(f"   Status: {data.get('message')}")
            print(f"\n   📱 SMS SHOULD BE SENT TO: {phone}")
            print(f"   From Twilio number: Check your .env TWILIO_PHONE_NUMBER")
            print(f"\n   ⏳ Check backend logs for SMS sending details")
        else:
            print(f"❌ Failed to trigger SOS: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print(f"\n📱 Expected SMS recipient: {phone}")
    print(f"📍 Location: 17.38, 78.38 (Hyderabad)")
    print(f"📞 Check your phone for SMS within 5-10 seconds")
    print(f"\n💡 If SMS doesn't arrive:")
    print(f"   1. Check backend terminal for errors")
    print(f"   2. Verify phone number is correct: {phone}")
    print(f"   3. Verify phone is verified in Twilio console")
    print(f"   4. Check Twilio account has credits")
    
    return True

if __name__ == "__main__":
    print("Starting direct API SOS test...\n")
    
    # Make sure backend is running
    try:
        response = requests.get("http://localhost:8000/docs")
        print("✅ Backend is running\n")
    except:
        print("❌ Backend is not running!")
        print("Start backend with: python -m uvicorn main:app --reload")
        exit(1)
    
    test_sos_with_phone()
