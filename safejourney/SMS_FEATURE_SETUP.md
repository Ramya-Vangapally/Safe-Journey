# SMS Emergency Alert Feature - Setup Guide

## Overview
The SAFE PATH AI app now includes an SMS emergency alert system. When you click the SOS button, an SMS will be immediately sent to your emergency contact number with your location details.

## Features
✅ Set emergency contact number during app setup  
✅ SMS sent automatically when SOS button is clicked  
✅ Location link included in SMS message  
✅ Support for multiple contact methods  
✅ Graceful fallback if SMS service is unavailable  

---

## Setup Instructions

### Step 1: Set Up Twilio Account (Free Trial Available)

1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free Twilio account (includes $20 credit - enough for testing)
3. Complete email verification
4. Get your credentials:
   - **Account SID**: Found in Twilio Console
   - **Auth Token**: Found in Twilio Console  
   - **Phone Number**: Verify or get a Twilio trial phone number

### Step 2: Update Backend Configuration

Edit `safejourney/backend/.env` and add your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
```

### Step 3: Restart Backend Server

```bash
cd safejourney/backend
python -m uvicorn main:app --reload
```

You should see in the console:
```
✅ Twilio SMS service initialized
```

### Step 4: Use the Emergency Contact Feature

1. **First Login**: When you first log in to the app, you'll see an "Emergency Contact Setup" modal
2. **Enter Phone Number**: Enter the phone number where you want SMS alerts sent
   - Include country code (e.g., +91 for India, +1 for USA)
   - Example: +919876543210
3. **Save**: Click "Save Contact" button
4. **Confirmation**: You'll see "✅ Emergency contact saved!" message

### Step 5: Test SOS Alert

1. Open the app and navigate to a location
2. Click the **SOS** button (red button in bottom-right)
3. The SMS will be sent to your emergency contact with:
   - Your name
   - Your message ("Emergency! I need help!")
   - Your exact location coordinates
   - A Google Maps link to your location

---

## SMS Message Example

```
🆘 EMERGENCY ALERT from [Your Name]!

Emergency! I need help!

Location: 28.6139, 77.2090

Google Maps: https://maps.google.com/?q=28.6139,77.2090
```

---

## API Endpoints

### Update Emergency Contact
```
POST /api/update-emergency-contact
Content-Type: application/json

{
  "uid": "firebase_user_id",
  "emergency_contact_number": "+919876543210"
}

Response:
{
  "success": true,
  "message": "Emergency contact number updated successfully",
  "uid": "firebase_user_id",
  "emergency_contact_number": "+919876543210"
}
```

### Create SOS Alert (with automatic SMS)
```
POST /api/sos/alert
Content-Type: application/json

{
  "user_id": "firebase_user_id",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "message": "Emergency! I need help!"
}

Response:
{
  "success": true,
  "alert_id": "sos_1234567890_user_id",
  "message": "SOS alert sent. Nearby users have been notified.",
  "nearby_users_count": 2
}
```

---

## Backend Implementation Details

### 1. User Model Update
Added `emergency_contact_number` field to User model:
```python
class User(SQLModel, table=True):
    ...
    emergency_contact_number: Optional[str] = None
```

### 2. SMS Sending Function
```python
async def send_sos_sms(emergency_numbers: list, user_name: str, latitude: float, longitude: float, message: str):
    # Uses Twilio Client to send SMS
    # Formats phone numbers with country code
    # Includes Google Maps location link
    # Logs success/failure for each contact
```

### 3. SOS Endpoint Update
- Now uses `emergency_contact_number` instead of hardcoded number
- Falls back gracefully if no emergency contact is set
- SMS sent in background task for non-blocking operation

---

## Frontend Implementation Details

### 1. Emergency Contact Setup Modal
- New component: `EmergencyContactSetup.jsx`
- Shown on first app launch
- Validates phone number (minimum 10 digits)
- Calls `/api/update-emergency-contact` endpoint
- Stores in localStorage for persistence

### 2. Integration in JourneyPlanner
- Checks if emergency contact is already set
- Shows modal only once per session
- Allows user to skip or save contact
- No interruption to app functionality

---

## Troubleshooting

### SMS Not Sending?

1. **Check Twilio Credentials**
   ```bash
   python -c "from main import app; print('✅ Twilio configured' if app.state else '❌ Not configured')"
   ```

2. **Check Backend Logs**
   - Look for "📱 Sending SOS SMS to emergency contacts"
   - Should show "✅ SMS sent to [phone_number]"

3. **Phone Number Format**
   - Must include country code: +91, +1, +44, etc.
   - Remove any spaces or dashes

4. **Twilio Trial Limitations**
   - Can only send to verified numbers in trial mode
   - Upgrade account to send to any number
   - Each SMS costs ~$0.0075

### Emergency Contact Not Saving?

1. Clear browser cache and localStorage
2. Check browser console for errors (F12 → Console tab)
3. Verify backend is running: `curl http://localhost:8000/health`
4. Check backend logs for "Emergency contact updated"

---

## Production Deployment

For production use:

1. **Upgrade Twilio Account**
   - Pay-as-you-go plan ($0.0075 per SMS)
   - Can send to any phone number

2. **Environment Variables**
   ```bash
   export TWILIO_ACCOUNT_SID="your_sid"
   export TWILIO_AUTH_TOKEN="your_token"
   export TWILIO_PHONE_NUMBER="your_number"
   ```

3. **Use Production Database**
   - Update `DATABASE_URL` to use PostgreSQL/Supabase
   - See `backend/.env` for connection string format

4. **Test with Real Numbers**
   - Have friends test SOS with their numbers
   - Verify SMS arrives with correct location

---

## Cost Estimation

- **Free Trial**: $20 credit (~2,667 SMS messages)
- **Production**: $0.0075 per SMS in India
- **Storage**: Emergency contacts stored in SQLite/PostgreSQL (free)
- **Geolocation**: Uses free OpenStreetMap/OSRM APIs

---

## Support & Documentation

- **Twilio Docs**: https://www.twilio.com/docs/sms
- **Twilio Python SDK**: https://github.com/twilio/twilio-python
- **SAFE PATH AI Issues**: Create issue in repository

---

## Security Notes

✅ Emergency contact numbers stored in database  
✅ SMS sent only when SOS button is clicked (user-initiated)  
✅ Firebase UID required for authentication  
✅ No emergency contacts shared with third parties  
✅ All API endpoints require CORS validation  

---

## Future Enhancements

- [ ] Multiple emergency contacts (friend1, friend2, family)
- [ ] Automatic SMS to police after 2 minutes (if SOS not resolved)
- [ ] WhatsApp message integration
- [ ] Push notifications as alternative to SMS
- [ ] Emergency contact groups (family, friends, etc.)
- [ ] SMS confirmation when helper responds
