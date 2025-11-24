# Firebase Setup Guide

This guide will help you set up Firebase for the Safe Journey application.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard:
   - Enter a project name
   - (Optional) Enable Google Analytics
   - Click "Create project"

## Step 2: Enable Authentication

1. In Firebase Console, go to **Authentication** > **Get started**
2. Click on **Sign-in method** tab
3. Enable **Email/Password** authentication
4. Click "Save"

## Step 3: Set Up Firestore Database

1. In Firebase Console, go to **Firestore Database** > **Create database**
2. Choose **Start in test mode** (for development)
3. Select a location for your database
4. Click "Enable"

### Firestore Security Rules (Development)

For development, you can use these rules. **Update them for production!**

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // SOS Alerts collection
    match /sosAlerts/{alertId} {
      allow create: if request.auth != null;
      allow read: if request.auth != null;
    }
  }
}
```

## Step 4: Set Up Realtime Database (for Location Sharing)

1. In Firebase Console, go to **Realtime Database** > **Create database**
2. Choose **Start in test mode**
3. Select a location (same as Firestore recommended)
4. Click "Enable"

### Realtime Database Rules (Development)

```
{
  "rules": {
    "locations": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

## Step 5: Get Firebase Configuration

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Scroll down to **Your apps** section
3. Click on the **Web** icon (`</>`)
4. Register your app (e.g., "Safe Journey Web")
5. Copy the Firebase configuration object

## Step 6: Configure the Application

1. Open `src/config/firebase.js`
2. Replace the placeholder values with your Firebase config:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  databaseURL: "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com"
}
```

## Step 7: Enable Required APIs

Make sure the following APIs are enabled in your Firebase/Google Cloud project:

- **Authentication API** (already enabled with Firebase Auth)
- **Cloud Firestore API**
- **Realtime Database API**

## Features Implemented

### ✅ Firebase Authentication
- User registration with email/password
- User login
- User logout
- Session persistence

### ✅ Firestore Database
- User profiles stored in `users` collection
- SOS alerts stored in `sosAlerts` collection
- User data includes: fullName, email, phone, credits, timestamps

### ✅ Realtime Database
- Real-time location sharing
- Active user locations tracked
- Location updates every 30 seconds

### ✅ SOS Emergency Service
- SOS alerts saved to Firestore
- Location data included
- Ready for integration with SMS/email services

## Production Considerations

1. **Update Security Rules**: Modify Firestore and Realtime Database rules for production
2. **Enable App Check**: Add Firebase App Check for additional security
3. **SMS Integration**: Integrate Twilio or similar service for SOS alerts
4. **Email Notifications**: Set up Firebase Cloud Functions for email notifications
5. **Rate Limiting**: Implement rate limiting for SOS alerts
6. **Data Privacy**: Ensure compliance with data protection regulations

## Troubleshooting

### Authentication Issues
- Verify Email/Password is enabled in Firebase Console
- Check that API keys are correct in `firebase.js`

### Firestore Issues
- Ensure Firestore is created and enabled
- Check security rules allow authenticated users

### Realtime Database Issues
- Ensure Realtime Database is created
- Check database URL is correct in config
- Verify security rules

## Next Steps

- [ ] Set up Firebase Cloud Functions for SOS notifications
- [ ] Integrate Twilio for SMS alerts
- [ ] Add email notifications via SendGrid or similar
- [ ] Implement emergency contact management
- [ ] Add push notifications via Firebase Cloud Messaging

