# ✅ Preferences Page Added

## What's New

A new **Preferences Page** appears after user login asking for:

1. **Gender** - Male, Female, Other (3 button options)
2. **Age Group** - Dropdown with age ranges (13-17, 18-25, 26-35, 36-45, 46-55, 56+)
3. **Means of Transport** - Walking or Transport (2 button options)
4. **Time Usage** - Checkboxes for when they use the transport:
   - 🌅 Morning (6 AM - 12 PM)
   - ☀️ Afternoon (12 PM - 6 PM)
   - 🌆 Evening (6 PM - 9 PM)
   - 🌙 Night (9 PM - 6 AM)

---

## Features

✅ **Frontend Only** - No backend storage
✅ **Session Storage** - Preferences marked as completed in session
✅ **Optional** - Users can skip preferences
✅ **Beautiful UI** - Matches dark theme with cyan/blue gradients
✅ **Responsive** - Works on mobile and desktop
✅ **Validation** - Ensures fields are filled before continuing

---

## Flow

```
Login → Preferences Page → Journey Planner
```

- User logs in
- Redirected to `/preferences`
- User fills preferences (or skips)
- User continues to `/journey-planner`
- On next login, preferences page shows again (can be changed)

---

## File Structure

```
PreferencesPage.jsx
  ├── Gender selection (Male/Female/Other)
  ├── Age dropdown (6 ranges)
  ├── Transport mode (Walking/Transport)
  ├── Time checkboxes (Morning/Afternoon/Evening/Night)
  ├── Skip button
  └── Continue button
```

---

## How It Works

### Selection Behavior
- **Gender/Transport**: Single selection (radio-style buttons)
- **Age**: Dropdown single selection
- **Time**: Multiple selections (checkboxes)

### Validation
- All fields required before continue
- At least one time period must be selected
- Error message shows if validation fails

### Storage
- **NOT stored in database** ✅
- **NOT stored in localStorage** ✅
- **Only in sessionStorage** (session-based only)
- Marked as `preferencesCompleted` in session

### Skip Option
- Users can skip preferences
- Preferences page shown again on next login
- Skipping takes user directly to journey planner

---

## UI Components

### Colors
- Primary: Cyan (#06b6d4)
- Secondary: Blue (#3b82f6)
- Background: Dark slate (#0f172a)
- Hover: Lighter cyan/slate

### Layout
- Centered form on dark gradient background
- 2-column layout on desktop
- Single column on mobile
- Maximum width: 896px (2xl)

### Typography
- Header: 4xl bold with gradient text
- Labels: lg bold cyan
- Input: Medium text on dark background
- Helper text: Small slate text

---

## Styling

```jsx
// Gender/Transport buttons
bg-cyan-500 (selected)
bg-slate-700 (unselected)
rounded-lg with border transitions

// Age dropdown
bg-slate-700
border-slate-600
focus: border-cyan-400, ring-cyan-400

// Time checkboxes
Custom checkbox styling
accent-cyan-500
Checkbox animation on hover
```

---

## Component Props

```jsx
<PreferencesPage 
  onComplete={callback}  // Called when user completes preferences
/>
```

- `onComplete`: Function called when Continue is clicked
- Navigates to `/journey` if no callback provided

---

## State Structure

```javascript
{
  gender: 'Male' | 'Female' | 'Other',
  age: '13-17' | '18-25' | '26-35' | '36-45' | '46-55' | '56+',
  transport: 'Walking' | 'Transport',
  transportTimes: {
    morning: boolean,
    afternoon: boolean,
    evening: boolean,
    night: boolean
  }
}
```

---

## Routing

Updated routes in `App.jsx`:

```jsx
/login          → AuthPage
/preferences    → PreferencesPage (after login)
/journey-planner → JourneyPlanner
/journey        → JourneyPlanner (alias)
/route/:routeId → SingleRouteView
```

---

## Session Management

Session variables:
- `preferencesCompleted` - Set to 'true' when user completes
- Cleared on logout

---

## Testing

### Via App
1. Start backend: `python -m uvicorn main:app --reload`
2. Start frontend: `npm run dev`
3. Login
4. Should see Preferences Page
5. Fill or skip preferences
6. Should go to Journey Planner

### Manual Route
```
http://localhost:5173/preferences
```

---

## Customization

### Add More Fields
Edit `PreferencesPage.jsx` state and form sections

### Change Styling
Update Tailwind classes in component JSX

### Add Backend Storage
Add POST endpoint in backend to save preferences

### Change Time Periods
Modify `transportTimes` checkboxes section

---

## Notes

- ✅ No backend changes required
- ✅ Pure frontend component
- ✅ SessionStorage (not persistent across sessions)
- ✅ Can be extended later with backend storage
- ✅ Beautiful dark theme matching app design
- ✅ Mobile responsive

---

## Future Enhancements

Could add:
- Backend storage of preferences (make persistent)
- Use preferences to customize routes/recommendations
- Safety insights based on age group
- Route recommendations based on transport mode
- Alerts during user's usual travel times
