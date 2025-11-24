# Safe Journey 🛡️

A professional dark-themed web application for safe navigation with route planning and safety scoring.

## Features

- **Login/Register System**: Secure authentication with mock database (ready for Firebase integration)
- **Journey Planner**: Interactive route planning with multiple route options
- **Safety Scoring**: AI-powered safety score calculation based on lighting, police presence, active users, traffic, and distance
- **Google Maps Integration**: Dark mode map with route visualization
- **SOS Functionality**: Emergency alert system
- **Responsive Design**: Works on all screen sizes

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- React Router
- Google Maps JavaScript API

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Get Google Maps API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Maps JavaScript API
   - Create an API key
   - Replace `YOUR_API_KEY` in `index.html` with your actual API key

3. **Run Development Server**
   ```bash
   npm run dev
   ```

4. **Build for Production**
   ```bash
   npm run build
   ```

## Project Structure

```
src/
├── components/
│   ├── AuthPage.jsx          # Login/Register page
│   ├── JourneyPlanner.jsx    # Main journey planning interface
│   ├── MapContainer.jsx      # Google Maps integration
│   ├── RouteCard.jsx         # Individual route display card
│   ├── BottomDrawer.jsx      # Expandable drawer with SOS/report/share
│   └── SingleRouteView.jsx   # Single route view with SOS
├── utils/
│   ├── auth.js              # Authentication functions
│   └── safetyScore.js       # Safety score calculation
├── App.jsx                  # Main app with routing
├── main.jsx                 # Entry point
└── index.css                # Global styles
```

## Safety Score Formula

The safety score is calculated using:

```
SafetyScore = (L * 0.25) + (P * 0.25) + (U * 0.25) + ((10 - T) * 0.15) + ((10 - D/2) * 0.10)
```

Where:
- `L` = Lighting (0-10)
- `P` = Police Presence (0-10)
- `U` = Active Users (0-10)
- `T` = Traffic (0-10)
- `D` = Distance (km)

**Categories:**
- 🟢 Safe Route: Score ≥ 8.0
- 🟡 Moderate Route: 6.0 ≤ Score < 8.0
- 🔴 Risky Route: Score < 6.0

## Mock Data

Currently, the app uses mock data stored in localStorage. To integrate with a real backend:

1. Update `src/utils/auth.js` to use your authentication API
2. Update route generation in `src/utils/safetyScore.js` to fetch from your API
3. Replace mock route paths with actual DirectionsService calls in `MapContainer.jsx`

## Notes

- The app uses localStorage for user data and authentication (mock database)
- Google Maps requires a valid API key with billing enabled
- Location services require user permission
- All routes are currently generated with mock data

## License

MIT

