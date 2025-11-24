"""
Debug: Check if backend is correctly reading emergency contact from database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from models import User
from database import engine
from datetime import datetime

print("=" * 70)
print("DEBUG: Emergency Contact in Database")
print("=" * 70)

try:
    session = Session(engine)
    
    # Get all users
    users = session.exec(select(User)).all()
    
    if not users:
        print("\n❌ No users in database!")
        print("   Create a user by:")
        print("   1. Opening the app")
        print("   2. Logging in (creates user)")
        print("   3. Setting emergency contact")
        session.close()
        sys.exit(1)
    
    print(f"\n✅ Found {len(users)} user(s) in database:\n")
    
    for i, user in enumerate(users, 1):
        print(f"{i}. User: {user.uid}")
        print(f"   Display Name: {user.display_name or 'Not set'}")
        print(f"   Email: {user.email or 'Not set'}")
        print(f"   Emergency Contact: {user.emergency_contact_number or '❌ NOT SET'}")
        print(f"   Phone: {user.phone or 'Not set'}")
        print(f"   Location: ({user.latitude}, {user.longitude}) or Not set")
        print(f"   Credits: {user.credits}")
        print()
    
    # Check specifically which users have emergency contacts
    users_with_contact = [u for u in users if u.emergency_contact_number]
    users_without_contact = [u for u in users if not u.emergency_contact_number]
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Users WITH emergency contact: {len(users_with_contact)}")
    for u in users_with_contact:
        print(f"  • {u.uid}: {u.emergency_contact_number}")
    
    print(f"\nUsers WITHOUT emergency contact: {len(users_without_contact)}")
    for u in users_without_contact:
        print(f"  • {u.uid}: ⚠️  Emergency contact not set")
    
    if users_without_contact:
        print("\n💡 TO FIX: Set emergency contact in app for these users")
        print("   1. Login as this user in the app")
        print("   2. Set emergency contact in modal")
        print("   3. Then SOS will send SMS")
    
    session.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("When you click SOS, backend will:")
print("1. Look up user by UID")
print("2. Read emergency_contact_number from database")
print("3. Send SMS to that number")
print("=" * 70)
