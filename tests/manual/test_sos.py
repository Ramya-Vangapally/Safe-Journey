#!/usr/bin/env python3
"""
Test script for SOS alert functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_sos_alert():
    """Test the SOS alert endpoint"""
    print("🧪 Testing SOS Alert Endpoint...")
    
    # Test data
    sos_data = {
        "user_id": "test_user_001",
        "latitude": 17.397154,
        "longitude": 78.49001,
        "message": "Test emergency - Please help!"
    }
    
    try:
        print(f"\n📤 Sending SOS alert request:")
        print(json.dumps(sos_data, indent=2))
        
        response = requests.post(
            f"{BASE_URL}/api/sos/alert",
            json=sos_data,
            timeout=10
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📋 Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎉 SOS Alert Created Successfully!")
            print(f"   Alert ID: {result.get('alert_id')}")
            print(f"   Nearby users notified: {result.get('nearby_users_count')}")
            print(f"   Police alert scheduled: {result.get('police_alert_scheduled')}")
            
            # Check if SMS was sent (should see in console/logs)
            print(f"\n📱 Check backend console for SMS sending logs...")
            print(f"   Expected: '✅ SOS SMS sent successfully' or '📱 [SOS SMS ALERT]'")
        else:
            print(f"\n❌ Request failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_get_sos_alerts():
    """Test getting active SOS alerts"""
    print("\n" + "="*60)
    print("🧪 Testing Get Active SOS Alerts...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/sos/alerts",
            timeout=10
        )
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"📋 Active SOS Alerts:")
        print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 SafeJourney SOS Alert Test Suite")
    print("="*60)
    
    test_sos_alert()
    test_get_sos_alerts()
    
    print("\n" + "="*60)
    print("✅ Tests complete!")
    print("\n📝 Next Steps:")
    print("   1. Check backend console for SMS alert logs")
    print("   2. Verify location coordinates in test data")
    print("   3. Check if nearby users were found in segment")
    print("   4. If SMS service is configured, verify SMS was sent to 6303369449")
