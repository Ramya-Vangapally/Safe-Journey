# SafeJourney

SafeJourney is a full-stack personal safety and navigation app that combines route planning, live location sharing, safety scoring, and SOS/SMS emergency workflows.

## What This Project Includes

- Frontend web app (React + Vite + Leaflet)
- Backend API (FastAPI + SQLModel)
- Firebase authentication and realtime location sharing
- Route search and navigation support (OSRM + Nominatim)
- Segment-based safety scoring and incident reporting
- SOS alert flow with optional Twilio SMS integration

## Repository Layout

```text
Safe-Journey/
  safejourney/
    backend/    # FastAPI application and data layer
    frontend/   # React application
  *.md          # Project notes, SOS/SMS setup guides, verification docs
```

## Tech Stack

### Frontend
- React 18
- Vite 5
- Tailwind CSS
- React Router
- Leaflet + React Leaflet
- Firebase SDK

### Backend
- FastAPI
- Uvicorn
- SQLModel + SQLAlchemy
- SQLite (default local) or PostgreSQL/Supabase
- Twilio (optional, for SMS)

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Internet access (for map tiles, OSRM, Nominatim)
- Optional: Supabase/PostgreSQL connection string
- Optional: Twilio account for SMS sending

## Quick Start

### 1) Backend setup

```bash
cd safejourney/backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in `safejourney/backend`:

```env
# Database (optional). If omitted, SQLite file safejourney.db is used.
DATABASE_URL=

# Twilio (optional, needed only for SMS)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Optional integrations used by SOS service
TWILIO_PHONE=
FAST2SMS_API_KEY=
SOS_WEBHOOK_URL=
```

Run backend:

```bash
uvicorn main:app --reload --port 8000
```

API docs:
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 2) Frontend setup

```bash
cd safejourney/frontend
npm install
npm run dev
```

Frontend runs on Vite default port (usually http://localhost:5173).

## Configuration Notes

- Frontend currently calls backend at `http://localhost:8000` from utility modules.
- Backend defaults to SQLite if `DATABASE_URL` is not set.
- Firebase config is stored in `safejourney/frontend/src/config/firebase.js`.
- SOS SMS requires Twilio variables to be configured.

## Core Features

- User auth and profile bootstrapping
- Preferences page before journey planning
- Place search and route generation
- Safety score per route segment
- Live location updates to backend and Firebase Realtime DB
- Incident reporting that updates segment safety scores
- Emergency contact setup and validation
- SOS alert flow:
  - create alert
  - nearby user response flow
  - resolve alert
  - active SOS monitoring

## Key Backend Endpoints

- `POST /api/update-location`
- `POST /api/update-emergency-contact`
- `GET /api/check-emergency-contact`
- `POST /api/routes`
- `GET /api/search`
- `GET /api/active-users`
- `POST /api/reports`
- `GET /api/segments/{segment_id}/reports`
- `GET /api/segments/by-location`
- `POST /api/sos/alert`
- `POST /api/sos/respond`
- `POST /api/sos/resolve`
- `GET /api/sos/active`
- `GET /health`
