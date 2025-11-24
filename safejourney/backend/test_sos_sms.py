"""
Test SOS SMS Feature - Simulates complete flow
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from sqlmodel import Session, select
from models import User
from database import engine
import asyncio
from datetime import datetime

load_dotenv()

async def test_sos_sms():
    """Test the complete SOS SMS flow"""
    
    print("=" * 70)
    print("TEST: SOS SMS Feature")
    print("=" * 70)
    
    # Check Twilio config
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    print("\n1️⃣ CHECKING TWILIO CONFIGURATION")
    print("-" * 70)
    print(f"Account SID: {TWILIO_ACCOUNT_SID[:15]}..." if TWILIO_ACCOUNT_SID else "❌ NOT SET")
    print(f"Auth Token: {TWILIO_AUTH_TOKEN[:15]}..." if TWILIO_AUTH_TOKEN else "❌ NOT SET")
    print(f"Phone Number: {TWILIO_PHONE_NUMBER}")
    
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER):
        print("❌ TWILIO CONFIGURATION MISSING")
        return False
    
    try:
        from twilio.rest import Client
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("✅ Twilio client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Twilio: {e}")
        return False
    
    # Get phone number from user
    print("\n2️⃣ ENTER YOUR PHONE NUMBER")
    print("-" * 70)
    user_phone = input("Enter your phone number (with country code, e.g., +919876543210): ").strip()
    
    if not user_phone:
        print("❌ Phone number required")
        return False
    
    # Check database
    print("\n3️⃣ CHECKING DATABASE & USER")
    print("-" * 70)
    
    try:
        session = Session(engine)
        
        # Create or get test user
        test_uid = "test_sos_user_123"
        test_email = f"{test_uid}@test.com"
        
        user = session.exec(select(User).where(User.uid == test_uid)).first()
        
        if not user:
            user = User(
                uid=test_uid,
                email=test_email,
                display_name="Test User",
                latitude=17.38,
                longitude=78.38,
                credits=100000,
                last_active_at=datetime.utcnow(),
                emergency_contact_number=user_phone
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"✅ Created test user: {test_uid}")
        else:
            print(f"✅ Found existing test user: {test_uid}")
            # Update emergency contact
            user.emergency_contact_number = user_phone
            session.add(user)
            session.commit()
            session.refresh(user)
        
        # Check emergency contact
        print(f"\n   User emergency contact: {user.emergency_contact_number or '❌ NOT SET'}")
        print(f"   User phone: {user.phone or '❌ NOT SET'}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test SMS sending
    print("\n4️⃣ TESTING SMS SENDING")
    print("-" * 70)
    
    emergency_numbers = [user.emergency_contact_number, user.phone]
    emergency_numbers = [num for num in emergency_numbers if num]  # Remove None values
    
    if not emergency_numbers:
        print("❌ NO EMERGENCY NUMBERS TO TEST")
        print("   Set emergency_contact_number for user first")
        return False
    
    print(f"Emergency numbers to test: {emergency_numbers}")
    
    latitude = 17.38
    longitude = 78.38
    user_name = user.display_name or user.uid
    message = "Emergency! I need help!"
    
    sms_body = f"🆘 EMERGENCY ALERT from {user_name}!\n\n{message}\n\nLocation: {latitude}, {longitude}\n\nGoogle Maps: https://maps.google.com/?q={latitude},{longitude}"
    
    print(f"\nSMS Content:")
    print(f"  From: {TWILIO_PHONE_NUMBER}")
    print(f"  Body:\n{sms_body}")
    
    successful_sends = 0
    failed_sends = 0
    
    for phone_number in emergency_numbers:
        try:
            # Format phone number
            if not phone_number.startswith('+'):
                formatted_number = f"+91{phone_number.lstrip('0')}"
            else:
                formatted_number = phone_number
            
            print(f"\n  📱 Sending to {formatted_number}...")
            
            message_obj = twilio_client.messages.create(
                body=sms_body,
                from_=TWILIO_PHONE_NUMBER,
                to=formatted_number
            )
            
            print(f"     ✅ SMS SENT!")
            print(f"     Message SID: {message_obj.sid}")
            print(f"     Status: {message_obj.status}")
            successful_sends += 1
            
        except Exception as e:
            print(f"     ❌ FAILED: {str(e)}")
            failed_sends += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n✅ Successful SMS sends: {successful_sends}")
    print(f"❌ Failed SMS sends: {failed_sends}")
    
    if successful_sends > 0:
        print("\n🎉 SUCCESS! SMS feature is working!")
        return True
    else:
        print("\n❌ ISSUE: SMS could not be sent")
        print("\nCommon issues:")
        print("  1. Emergency contact number not verified in Twilio")
        print("  2. Invalid phone number format")
        print("  3. Twilio account doesn't have SMS capability")
        print("  4. Account has insufficient credits")
        print("  5. Phone number in 'To' field is blocked or invalid")
        return False

if __name__ == "__main__":
    print("Starting SOS SMS test...\n")
    success = asyncio.run(test_sos_sms())
    sys.exit(0 if success else 1)
