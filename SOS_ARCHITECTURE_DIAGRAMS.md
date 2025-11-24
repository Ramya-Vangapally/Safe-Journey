# 🚨 SafeJourney SOS System - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SafeJourney SOS System                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   Frontend (React)   │◄────────►│   Backend (FastAPI)  │
│                      │          │                      │
│  - SOS Button        │          │  - /api/sos/alert    │
│  - User Location     │  HTTP    │  - /api/sos/respond  │
│  - Alert Status      │  REST    │  - /api/sos/resolve  │
│                      │          │                      │
└──────────────────────┘         └──────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
            ┌──────────────────┐ ┌────────────────┐ ┌──────────────┐
            │ SOS Service      │ │ Database Ops   │ │ Background   │
            │ (sos_alert_...) │ │ (Segments)     │ │ Tasks        │
            │                  │ │                │ │              │
            └──────────────────┘ └────────────────┘ └──────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌────────┐ ┌────────┐ ┌─────────────┐
    │ Twilio │ │Fast2SMS│ │Webhook/Log  │
    └────────┘ └────────┘ └─────────────┘
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
            ┌──────────────────┐
            │   Emergency SMS  │
            │   6303369449     │
            └──────────────────┘
```

## Request/Response Flow

### 1. SOS Alert Creation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Clicks SOS Button                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Confirmation     │
                    │ Dialog Shown     │
                    └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼ (Confirmed)       ▼ (Cancelled)
            ┌──────────────┐      [Nothing happens]
            │ Get location │
            │ (GPS/IP)     │
            └──────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ POST /api/sos/alert   │
        │ {                     │
        │   user_id: "...",     │
        │   latitude: 17.397,   │
        │   longitude: 78.490   │
        │ }                     │
        └───────────────────────┘
                    │
                    ▼
        ┌─────────────────────────────────────┐
        │ Backend: Create SOS Alert Record    │
        │ - Generate alert ID                 │
        │ - Find segment for location         │
        │ - Get nearby users in segment       │
        │ - Store alert in-memory             │
        └─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    [Background Task 1]  [Background Task 2]
    Send SMS to           Schedule Police
    Emergency Contacts    Alert (2 min)
        │                     │
        ▼                     ▼
    📱 SMS Sent           ⏰ Timer Started
    to 6303369449
        │                     │
        └───────────┬─────────┘
                    │
                    ▼
        ┌─────────────────────────────────────┐
        │ Return to User:                     │
        │ {                                   │
        │   success: true,                    │
        │   alert_id: "sos_1763240194_...",  │
        │   nearby_users_count: 0,            │
        │   police_alert_scheduled: true      │
        │ }                                   │
        └─────────────────────────────────────┘
                    │
                    ▼
        ┌─────────────────────────────────────┐
        │ Frontend Shows Success Message:     │
        │ "SOS Alert Sent!                    │
        │  Nearby users and police notified"  │
        └─────────────────────────────────────┘
```

## SMS Sending Flow

```
┌──────────────────────────────────────────────────────────────────┐
│        Background Task: Send SOS SMS                              │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ send_sos_sms() called  │
                  │ Emergency numbers:     │
                  │ ["6303369449"]         │
                  └────────────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ sos_service.send...()  │
                  │ Format message with:   │
                  │ - User name            │
                  │ - Google Maps link     │
                  │ - Coordinates          │
                  └────────────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ SMS Provider Check:    │
                  └────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
        ┌───────────▼─┐   ┌───▼────┐  ┌▼──────────┐
        │ Twilio Avail?    │Fast2SMS?   │Webhook?│
        └───┬──────┬──┘   └────────┘  └─────────┘
            │ YES  │ NO
            │      └──────┐
            ▼             │
      ┌──────────┐        │
      │ Try      │        │
      │ Twilio   │        │
      └──┬───────┘        │
         │ Success        │
         ▼                │
    ✅ SMS Sent      ┌────▼──────┐
                     │ Try        │
              ┌─────►│ Fast2SMS   │
              │      └────┬───────┘
              │ Fallback  │ Success
              │      ┌────▼──────┐
              │      │ ✅ SMS    │
              │      │ Sent      │
              │      └───────────┘
              │
              │
         ┌────▼──────────────┐
         │ Last Resort       │
         │ Print to console: │
         │ "[SOS SMS ALERT]" │
         │ Location + Phone  │
         └───────────────────┘
```

## Data Flow Sequence Diagram

```
User                Frontend              Backend             Database
 │                    │                      │                   │
 │ Click SOS          │                      │                   │
 ├───────────────────►│                      │                   │
 │                    │ Confirm Dialog       │                   │
 │                    │ (Location ready?)    │                   │
 │                    │                      │                   │
 │                    │ POST /api/sos/alert  │                   │
 │                    ├─────────────────────►│                   │
 │                    │ {user_id, lat, lng}  │                   │
 │                    │                      │ Find Segment      │
 │                    │                      ├──────────────────►│
 │                    │                      │ QUERY: segments   │
 │                    │                      │◄──────────────────┤
 │                    │                      │ segment_id        │
 │                    │                      │                   │
 │                    │                      │ Get Nearby Users  │
 │                    │                      ├──────────────────►│
 │                    │                      │ QUERY: users in   │
 │                    │                      │        segment    │
 │                    │                      │◄──────────────────┤
 │                    │                      │ user_ids: []      │
 │                    │                      │                   │
 │                    │ Store Alert          │                   │
 │                    │ (in-memory)          │                   │
 │                    │                      │                   │
 │ [Background Tasks  │                      │                   │
 │  Started]          │                      │                   │
 │                    │                      │ Task 1:           │
 │                    │                      │ Send SMS          │
 │                    │                      │                   │
 │                    │ ┌───────────────────┼────────────────┐  │
 │                    │ │ Task 2: Schedule  │                │  │
 │                    │ │ Police Alert      │                │  │
 │                    │ │ (2 min timer)     │                │  │
 │                    │ │                   │                │  │
 │                    │ │    ┌──────────────▼────┐           │
 │                    │ │    │ SMS Service       │           │
 │                    │ │    │ sos_service.send()│           │
 │                    │ │    └──────────────┬────┘           │
 │                    │ │                   │ API Call       │
 │ 📱 SMS Received    │ │    ┌──────────────▼────┐           │
 │ on 6303369449      │ │    │ Fast2SMS/Twilio   │           │
 │ w/ Alert Details   │ │    │ Provider          │           │
 │                    │ │    └───────────────────┘           │
 │                    │ │                                    │
 │                    │◄────────┐                            │
 │                    │ 200 OK  │                            │
 │ "SOS Sent!" Alert  │         │                            │
 │◄───────────────────┤         │                            │
 │ [Success Message]  │    ┌────▼──────┐                     │
 │                    │    │ Console   │                     │
 │                    │    │ Log:      │                     │
 │                    │    │ ✅ SMS    │                     │
 │                    │    │ sent to   │                     │
 │                    │    │ 6303369449│                     │
 │                    │    └───────────┘                     │
 │ ⏰ 2 minutes later:                                        │
 │                    │ Police Notification                  │
 │                    │ (automatic)                          │
 │                    │                                      │
 
Legend:
───► Sync HTTP request
····► Background async task
     Current focus
[  ] System event
```

## SMS Message Template

```
┌─────────────────────────────────────┐
│      🚨 SOS ALERT 🚨                 │
├─────────────────────────────────────┤
│                                     │
│  John Doe needs help!              │
│                                     │
│  Location:                          │
│  https://maps.google.com/?q=        │
│  17.397154,78.49001                 │
│                                     │
│  Coordinates:                       │
│  Latitude: 17.397154                │
│  Longitude: 78.49001                │
│                                     │
│  Please respond immediately!        │
│                                     │
│  [Sent from SafeJourney]            │
│  Time: 2025-11-16 02:28:34 UTC      │
│                                     │
└─────────────────────────────────────┘
```

## Error Handling Flow

```
┌────────────────────────────────────┐
│ SOS Alert Request Received         │
└────────────────────────────────────┘
         │
         ▼
    Validate Input:
    - user_id? ✓
    - lat/lng? ✓
    - User in DB? ✓
         │
    ┌────┴─────┐
    │           │
    ▼ No        ▼ Yes
  [Error]    Continue
    │           │
    │           ▼
    │       Find Segment
    │           │
    │       ┌───┴───┐
    │       │       │
    │    ▼ No    ▼ Yes
    │  [Error] Continue
    │           │
    │           ▼
    │       Get Nearby Users
    │           │
    │       ┌───┴───┐
    │       │       │
    │    Success  Error
    │       │       │
    │       ▼       ▼
    │     [OK]   [Logged]
    │           Continue
    │       ┌───┴───────┐
    │       │           │
    │       ▼           ▼
    │   Store       Schedule
    │   Alert       Police
    │       │           │
    │       ▼           ▼
    │   [Success]   [Success]
    │       │           │
    │       └───┬───────┘
    │           ▼
    │   Send SMS (Background)
    │           │
    │       ┌───┴──────────────┐
    │       │                  │
    │   ┌───▼───┐          ┌───▼────┐
    │   │ Error │          │ Success│
    │   │       │          │        │
    │   ▼       │          ▼        │
    │ Log err  │         Log msg   │
    │   │      │          │        │
    │   └──────┴──────────┴────────┘
    │                │
    └────────┬───────┘
             ▼
    Return 200 OK
    (always returns success)
```

## Configuration & Environment

```
┌──────────────────────────────────────┐
│   SOS System Environment Check       │
└──────────────────────────────────────┘
         │
         ▼
    FAST2SMS_API_KEY set?
         │
    ┌────┴────┐
    │          │
   YES        NO
    │          │
    ▼          ▼
  Use      Check TWILIO
  Fast2SMS  credentials
    │          │
    │      ┌───┴───┐
    │      │       │
    │    YES      NO
    │      │       │
    │      ▼       ▼
    │    Use    Check
    │   Twilio  Webhook
    │      │       │
    │      │   ┌───┴────┐
    │      │   │        │
    │      │  YES      NO
    │      │   │        │
    │      │   ▼        ▼
    │      │  Webhook Console Log
    │      │   │        │
    │      └──┬┴────────┴┘
    │         │
    └────┬────┘
         ▼
    SMS Service Selected
    Ready to Send
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Components                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ NavigationPanel.jsx                                     │  │
│ │ - SOS button (always visible)                           │  │
│ │ - Confirmation dialog                                   │  │
│ │ - Calls: sendSOSAlert()                                 │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ SingleRouteView.jsx                                     │  │
│ │ - SOS button (in bottom bar)                            │  │
│ │ - Confirmation dialog                                   │  │
│ │ - Calls: sendSOSAlert()                                 │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ sosService.js                                           │  │
│ │ - sendSOSAlert(location, userId, message)               │  │
│ │ - Calls backend /api/sos/alert endpoint                │  │
│ │ - Returns alert ID and status                           │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │
         │ HTTP REST
         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend Endpoints                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ POST /api/sos/alert                                          │
│  └─ Creates alert, sends SMS, notifies users                │
│                                                               │
│ GET /api/sos/alerts                                          │
│  └─ Retrieves all active SOS alerts                         │
│                                                               │
│ POST /api/sos/respond                                        │
│  └─ Helper responds to alert                                │
│                                                               │
│ POST /api/sos/resolve                                        │
│  └─ Resolves alert as handled                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │
         │ Python asyncio
         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Backend Services                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ SOSService (sos_alert_service.py)                           │
│  ├─ send_sos_alert()                                         │
│  ├─ _send_via_twilio()                                       │
│  ├─ _send_via_fast2sms()                                     │
│  └─ _send_via_webhook()                                      │
│                                                               │
│ SegmentUtils (segment_utils.py)                             │
│  ├─ get_segment_by_location()                                │
│  ├─ get_nearby_users_in_segment()                            │
│  └─ update_active_user_count()                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │
         │ Async/Await
         ▼
┌─────────────────────────────────────────────────────────────┐
│              External SMS Providers                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌──────────────────┐   ┌──────────────────┐                │
│ │ Twilio (Paid)    │   │ Fast2SMS (Free)  │                │
│ │ Premium SMS      │   │ India SMS        │                │
│ │ Reliability: ⭐⭐⭐  │   │ Reliability: ⭐⭐ │                │
│ └──────────────────┘   └──────────────────┘                │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐│
│ │ Webhook Service (Custom)                                 ││
│ │ Deploy your own SMS endpoint                             ││
│ │ http://your-webhook.com/sms                              ││
│ └──────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │
         │ HTTP/API
         ▼
┌─────────────────────────────────────────────────────────────┐
│          Emergency Contact Receives SMS                      │
│                                                               │
│  📱 6303369449                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🚨 SOS ALERT 🚨                                         ││
│  │                                                          ││
│  │ John Doe needs help!                                   ││
│  │ Location: maps.google.com/?q=17.397154,78.49001       ││
│  │ Coordinates: 17.397154, 78.49001                      ││
│  │                                                          ││
│  │ [Tap to open location]                                ││
│  │ [Call back]                                            ││
│  │ [Reply]                                                ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Local Development (Current)                     │
│                                                              │
│  Machine: C:\Users\vanga\Desktop\safejourney2               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Frontend (React)                                     │  │
│  │ npm run dev                                          │  │
│  │ localhost:5173                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│           │                                                 │
│           ▼ HTTP                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Backend (FastAPI)                                    │  │
│  │ uvicorn backend.main:app --reload                    │  │
│  │ localhost:8000                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│           │                                                 │
│           ▼ asyncio                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SOS Service (sos_alert_service.py)                   │  │
│  │ In-process async task handling                       │  │
│  └──────────────────────────────────────────────────────┘  │
│           │                                                 │
│           ▼ HTTP/API                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SMS Providers                                        │  │
│  │ - Fast2SMS API (https://fast2sms.com)               │  │
│  │ - Twilio API (https://api.twilio.com)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Key Takeaways**:
- ✅ Synchronous request, asynchronous SMS delivery
- ✅ Multiple SMS provider fallbacks
- ✅ Non-blocking background tasks
- ✅ User gets immediate response
- ✅ SMS sent in parallel
- ✅ Resilient error handling
