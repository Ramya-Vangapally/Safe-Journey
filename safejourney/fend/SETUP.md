# Quick Setup Guide

## Prerequisites

- Node.js 16+ installed
- npm or yarn package manager
- Google Maps API key (free tier available)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Get Google Maps API Key

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Navigate to "APIs & Services" > "Library"
4. Search for "Maps JavaScript API" and enable it
5. Go to "Credentials" and create a new API key
6. (Optional) Restrict the API key to your domain for security

### 3. Configure API Key

Open `index.html` and replace `YOUR_API_KEY` with your actual Google Maps API key:

```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=places,geometry"></script>
```

### 4. Run the Application

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the port Vite assigns)

### 5. Test the Application

1. **Register a new account:**
   - Click "Register" tab
   - Fill in: Full Name, Email, Phone, Password, Confirm Password
   - Click "Register"

2. **Login:**
   - Use the credentials you just created
   - Click "Login"

3. **Plan a Journey:**
   - Allow location access when prompted
   - Enter a destination
   - Click "Find Safe Routes"
   - View the 3 route options with safety scores
   - Click on a route to view it in detail

4. **Test SOS Feature:**
   - Select a route
   - Click the SOS button (will show an alert in mock mode)

## Troubleshooting

### Map Not Loading

- Check browser console for errors
- Verify API key is correct in `index.html`
- Ensure Maps JavaScript API is enabled in Google Cloud Console
- Check if billing is enabled (required for Google Maps API)

### Location Not Working

- Ensure browser location permissions are granted
- Use HTTPS or localhost (required for geolocation API)
- Check browser console for permission errors

### Routes Not Showing

- Routes are generated with mock data
- In production, you'll need to integrate with a routing service (Google Directions API)

## Next Steps (Completed ✅)

All the following features have been implemented:

- ✅ **Firebase Authentication**: Replaced mock authentication with Firebase Auth
  - User registration and login with email/password
  - Session persistence
  - See `FIREBASE_SETUP.md` for setup instructions

- ✅ **Google Directions API Integration**: Real routing data from Google Directions API
  - Fetches actual route alternatives
  - Displays real route paths on map
  - Geocoding for destination addresses

- ✅ **Firestore Database**: Connected to Firebase Firestore for user data
  - User profiles stored in Firestore
  - User credits and profile data
  - SOS alerts stored in database

- ✅ **Real-time Location Sharing**: Implemented with Firebase Realtime Database
  - Users share location in real-time
  - Active user locations displayed on map
  - Location updates every 30 seconds

- ✅ **SOS Emergency Service**: Integrated SOS alert system
  - SOS alerts saved to Firestore
  - Location data included in alerts
  - Ready for SMS/email integration

## Additional Setup Required

1. **Firebase Configuration**: 
   - Follow instructions in `FIREBASE_SETUP.md`
   - Add your Firebase config to `src/config/firebase.js`

2. **Google Maps API Key**: 
   - Ensure your API key has Directions API enabled
   - Add to `index.html` (already configured)

3. **Production Enhancements**:
   - Set up Firebase Cloud Functions for notifications
   - Integrate SMS service (Twilio) for SOS alerts
   - Configure email notifications
   - Update security rules for production

