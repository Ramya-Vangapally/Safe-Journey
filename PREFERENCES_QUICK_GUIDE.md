# 🎨 Preferences Page - Quick Overview

## What Was Added

A beautiful preferences page that users see after logging in.

```
┌─────────────────────────────────┐
│     Tell Us About You            │
│ Help us personalize your safety  │
│           journey                │
├─────────────────────────────────┤
│                                  │
│  Gender:  [Male] [Female] [Other]│
│                                  │
│  Age Group: [Dropdown ▼]         │
│                                  │
│  Transport: [Walking] [Transport]│
│                                  │
│  Times:  ☑ Morning               │
│         ☐ Afternoon              │
│         ☑ Evening                │
│         ☐ Night                  │
│                                  │
│  [Skip]  [Continue →]            │
└─────────────────────────────────┘
```

---

## User Flow

```
1. User Opens App
         ↓
2. Login with Firebase
         ↓
3. Sees Preferences Page ✨ (NEW)
         ↓
4. Fills: Gender, Age, Transport, Times
         ↓
5. Clicks Continue
         ↓
6. Goes to Journey Planner
```

---

## Features

| Feature | Details |
|---------|---------|
| **Gender** | Radio buttons: Male / Female / Other |
| **Age** | Dropdown: 6 age ranges (13-17 to 56+) |
| **Transport** | Radio buttons: Walking / Transport |
| **Times** | Checkboxes: Morning/Afternoon/Evening/Night |
| **Validation** | All fields required + at least 1 time |
| **Skip Option** | Users can skip and go directly to app |
| **Storage** | Frontend only (sessionStorage) |
| **Styling** | Dark theme with cyan/blue gradients |

---

## Implementation

### New File Created
- `PreferencesPage.jsx` - Complete preferences form component

### Updated Files
- `App.jsx` - Added routes for preferences page

### No Backend Changes
- ✅ Frontend only
- ✅ No database modifications needed
- ✅ Can be extended later

---

## How to Test

### Method 1: Via App Flow
```bash
# Terminal 1: Backend
python -m uvicorn main:app --reload

# Terminal 2: Frontend
npm run dev

# Then:
1. Go to http://localhost:5173
2. Login
3. See Preferences Page
4. Fill or skip
5. Continue to Journey Planner
```

### Method 2: Direct URL
```
http://localhost:5173/preferences
```

---

## Data Structure (Frontend Only)

```javascript
{
  gender: "Male",           // String
  age: "18-25",            // String
  transport: "Walking",    // String
  transportTimes: {
    morning: true,         // Boolean
    afternoon: false,
    evening: true,
    night: false
  }
}
```

**Note:** This data is NOT saved anywhere - only used for this session.

---

## UI Highlights

### Colors
- 🔵 Cyan for selected/focused
- ⚫ Dark slate for unselected
- ✨ Gradient backgrounds

### Layout
- Centered form card
- Mobile responsive
- Clean dark theme
- Smooth transitions

### User Experience
- Clear labels
- Helpful descriptions
- Time period emojis (🌅 🌆 🌙)
- Loading states
- Error messages

---

## File Details

### PreferencesPage.jsx (133 lines)
```jsx
✅ Gender selection (3 buttons)
✅ Age group dropdown
✅ Transport mode selection (2 buttons)
✅ Time period checkboxes (4 options)
✅ Form validation
✅ Skip & Continue buttons
✅ Beautiful styling with Tailwind
✅ Error handling
✅ Responsive design
```

### App.jsx Updates
```jsx
✅ Import PreferencesPage component
✅ Add preferences route (/preferences)
✅ Add session-based completion tracking
✅ Route: Login → Preferences → Journey Planner
```

---

## Customization Options

### Add More Fields
```jsx
// In state
const [preferences, setPreferences] = useState({
  gender: '',
  age: '',
  transport: '',
  transportTimes: {},
  // Add here: ↓
  phone: '',      // Add phone field
  language: '',   // Add language field
})
```

### Change Options
```jsx
// Gender options
{['Male', 'Female', 'Other', 'Prefer not to say'].map(...)}

// Transport options
{['Walking', 'Public Transport', 'Private Vehicle'].map(...)}
```

### Modify Times
```jsx
// Add more time periods
{ id: 'midday', label: '⏱️ Midday (2 PM - 4 PM)' },
```

### Backend Integration (Future)
```jsx
// Save to backend instead of sessionStorage
const response = await fetch('/api/save-preferences', {
  method: 'POST',
  body: JSON.stringify(preferences)
})
```

---

## Validation Rules

✅ **All fields must be selected** before continuing
✅ **At least one time period** must be checked
✅ **Age must be selected** from dropdown
✅ **Gender must be selected** (M/F/Other)
✅ **Transport must be selected** (Walking/Transport)

**Error message shows** if validation fails → User must fix

---

## Session Behavior

```javascript
// When user completes preferences
sessionStorage.setItem('preferencesCompleted', 'true')

// On next page visit
const prefs = sessionStorage.getItem('preferencesCompleted')
if (prefs) {
  // Skip preferences, go to journey planner
}

// On logout
sessionStorage.clear()  // Preferences cleared too
```

---

## Status

✅ **Complete and Working**
✅ **Frontend build passes**
✅ **Ready to test**
✅ **Beautiful UI**
✅ **Fully functional**

---

## Next Steps

1. **Test in app** - See preferences page after login
2. **Fill preferences** - Test form validation
3. **Continue** - Verify it goes to journey planner
4. **Customize** - Modify fields/styling if needed
5. **Extend** - Add backend storage when ready

---

## Files Modified

```
✅ Created: PreferencesPage.jsx
✅ Updated: App.jsx
✅ No changes: Backend
✅ No DB changes: Database
```

**Total Impact:** Small, focused, frontend-only addition! 🎉
