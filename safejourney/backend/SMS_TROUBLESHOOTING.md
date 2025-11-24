# 🔧 SMS NOT WORKING? TROUBLESHOOTING GUIDE

## Quick Diagnostics

Run these commands in order to diagnose the SMS issue:

### Step 1: Check Twilio Configuration
```bash
cd safejourney/backend
python test_sms_diagnostics.py
```

### Step 2: Test Full SOS SMS Flow
```bash
python test_sos_sms.py
```

---

## Common Issues & Solutions

### ❌ Issue 1: "No emergency contacts available"

**Symptom:** SMS not sent, backend shows "⚠️ No emergency contacts available"

**Root Cause:** User didn't set emergency contact number

**Solution:**
1. Go to your app
2. You should see emergency contact setup modal
3. Enter your phone number (+919876543210 or 9876543210)
4. Save
5. Try SOS again

---

### ❌ Issue 2: "Twilio not configured"

**Symptom:** Backend shows "⚠️ Twilio not configured, SMS service unavailable"

**Root Cause:** Missing or incorrect credentials in `.env`

**Solution:**
1. Check `.env` file in `safejourney/backend/`:
```
TWILIO_ACCOUNT_SID=AC09f5aea6a09a1faa9b27b19620a1a860
TWILIO_AUTH_TOKEN=22e967958bc6954dd84ef31edec936a5
TWILIO_PHONE_NUMBER=+1 256 901 8317
```

2. If missing, add them and restart backend:
```bash
python -m uvicorn main:app --reload
```

3. Check backend logs for: `✅ Twilio SMS service initialized`

---

### ❌ Issue 3: "Invalid phone number format"

**Symptom:** Error: "not in a valid phone number format"

**Root Cause:** Phone number format is incorrect

**Solutions:**

**For India numbers:**
- ✅ Correct: `+919876543210` (with country code)
- ❌ Wrong: `9876543210` (without country code)
- ❌ Wrong: `91 98765 43210` (spaces)

**For US numbers:**
- ✅ Correct: `+14155552671` (with country code)
- ❌ Wrong: `4155552671` (without country code)

---

### ❌ Issue 4: "Invalid credentials"

**Symptom:** Error: "Authentication failed" or "Invalid credentials"

**Root Cause:** Wrong SID or Auth Token

**Solution:**
1. Go to https://www.twilio.com/console
2. Copy correct **Account SID** and **Auth Token**
3. Update `.env` file
4. Restart backend

---

### ❌ Issue 5: "Invalid 'From' Phone Number"

**Symptom:** Error: "Invalid 'From' Phone Number" or "Invalid 'From' number"

**Root Cause:** TWILIO_PHONE_NUMBER is not registered in your Twilio account

**Solution:**
1. Go to https://www.twilio.com/console/phone-numbers/incoming
2. Verify your phone number is listed
3. Copy exact phone number from Twilio (including country code and spaces if shown)
4. Update TWILIO_PHONE_NUMBER in `.env`
5. Restart backend

---

### ❌ Issue 6: "Phone number not verified"

**Symptom:** Error: "is not a valid phone number"

**Root Cause:** Emergency contact number not verified in Twilio

**Solution:**
1. Go to https://www.twilio.com/console/phone-numbers/verified
2. Add your phone number (+919876543210)
3. Verify with OTP
4. Then use same number in app emergency contact

---

### ❌ Issue 7: "Account doesn't have phone capability"

**Symptom:** Error: "Account does not have phone capability"

**Root Cause:** Twilio account not upgraded

**Solution:**
1. Upgrade your Twilio account to paid
2. Visit https://www.twilio.com/console/account/upgrade
3. Add payment method
4. Wait 5-10 minutes for account to be activated

---

### ❌ Issue 8: No account credit

**Symptom:** SMS silently fails, appears to send but doesn't arrive

**Root Cause:** Twilio account has no credits

**Solution:**
1. Check account balance: https://www.twilio.com/console/account/billing
2. Add credits if needed
3. Each SMS costs approximately $0.0075 - $0.015

---

## Verification Checklist

- [ ] TWILIO_ACCOUNT_SID set in .env
- [ ] TWILIO_AUTH_TOKEN set in .env
- [ ] TWILIO_PHONE_NUMBER set in .env
- [ ] Backend restarted after .env changes
- [ ] Backend shows: "✅ Twilio SMS service initialized"
- [ ] User has emergency contact set in app
- [ ] Emergency contact number is verified in Twilio
- [ ] Twilio account has SMS capability
- [ ] Twilio account has sufficient credits
- [ ] Emergency contact number in correct format (+country_code)

---

## Testing SMS Manually

### In Python Terminal:
```python
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

message = client.messages.create(
    body="Test SMS from SafeJourney!",
    from_=os.getenv("TWILIO_PHONE_NUMBER"),
    to="+919876543210"  # Your phone number
)

print(f"Message SID: {message.sid}")
print(f"Status: {message.status}")
```

---

## Check Backend Logs for SMS

When you click SOS button, you should see in backend terminal:

```
======================================================================
📱 SOS SMS SENDING PROCESS STARTED
======================================================================
✓ Emergency numbers to notify: ['+919876543210']
✓ Twilio client is initialized
✓ Sending from: +1 256 901 8317
✓ SMS Message:
🆘 EMERGENCY ALERT from User ABC123!
...
📤 Sending SMS to +919876543210...
   ✅ SMS SENT SUCCESSFULLY!
   Message SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Status: queued
```

---

## Still Not Working?

### Run diagnostic script:
```bash
python test_sms_diagnostics.py
```

### Run full SOS SMS test:
```bash
python test_sos_sms.py
```

### Check what gets logged:

1. **Backend logs** when starting:
   - Should show: `✅ Twilio SMS service initialized`

2. **Backend logs** when setting emergency contact:
   - Should show: `✅ Emergency contact updated for user ...`

3. **Backend logs** when clicking SOS:
   - Should show SMS sending process details

---

## Contact Twilio Support

If everything looks correct but SMS still doesn't work:

1. Go to https://www.twilio.com/console/support
2. Create support ticket
3. Include:
   - Account SID
   - Phone numbers being used
   - Error messages from backend
   - Recent SOS attempts

---

## Alternative: Use Twilio API Directly

If backend SMS isn't working, test Twilio directly:

1. Open command prompt
2. Run:
```bash
curl -X POST https://api.twilio.com/2010-04-01/Accounts/AC09f5aea6a09a1faa9b27b19620a1a860/Messages.json \
  -d "To=+919876543210" \
  -d "From=+1 256 901 8317" \
  -d "Body=Test from SafeJourney" \
  -u AC09f5aea6a09a1faa9b27b19620a1a860:22e967958bc6954dd84ef31edec936a5
```

This tests if Twilio API itself works.

---

## Summary

SMS flow:
1. User sets emergency contact in app ✅
2. App sends POST to `/api/update-emergency-contact` ✅
3. Backend saves to database ✅
4. User clicks SOS ✅
5. App sends POST to `/api/sos/alert` ✅
6. Backend checks if emergency contact exists ✅
7. Backend queues SMS background task ✅
8. Twilio sends SMS ❓ (This is where it might fail)

If SMS isn't going, it's usually step 8 - Twilio configuration or account issues.

Run the diagnostic scripts to pinpoint exactly where it fails!
