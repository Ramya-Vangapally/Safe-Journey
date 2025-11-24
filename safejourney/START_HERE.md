# 🚀 SafeJourney App - Installation & Startup Guide

## ✅ Required Dependencies

### **1. System Requirements**
- **Python 3.10+** (for backend)
- **Node.js 18+** and **npm 10+** (for frontend)
- **PostgreSQL Database** (Supabase - already configured)
- **Firebase Account** (for authentication - already configured)

---

## 📦 Installation Commands

### **Backend (Python)**

```bash
cd backend
pip install -r requirements.txt
```

**Key Backend Dependencies:**
- `fastapi==0.121.0` - Web framework
- `uvicorn==0.38.0` - ASGI server
- `sqlmodel==0.0.27` - Database ORM
- `psycopg2-binary==2.9.11` - PostgreSQL driver
- `httpx==0.28.1` - HTTP client (for OSRM & Nominatim)
- `polyline==1.4.0` - Route encoding
- `pydantic==2.12.4` - Data validation

### **Frontend (Node.js)**

```bash
cd fend
npm install
```

**Key Frontend Dependencies:**
- `react@^18.2.0` - React framework
- `react-dom@^18.2.0` - React DOM
- `react-leaflet@^4.2.1` - Leaflet maps for React
- `leaflet@^1.9.4` - Open-source mapping library
- `firebase@^12.5.0` - Firebase SDK
- `react-router-dom@^6.20.0` - Routing
- `vite@^5.0.8` - Build tool
- `tailwindcss@^3.3.6` - CSS framework

---

## 🔧 Configuration Check

### **Backend Configuration**
✅ **Database:** Already configured in `backend/database.py`
- PostgreSQL (Supabase) connection is set up
- User table will be created automatically

✅ **OSRM Routing:** Public server (no API key needed)
- `http://router.project-osrm.org`

✅ **Nominatim Search:** Public server (no API key needed)
- `https://nominatim.openstreetmap.org`

### **Frontend Configuration**
✅ **Firebase:** Already configured in `fend/src/config/firebase.js`
- Authentication enabled
- Firestore database enabled
- Realtime Database enabled

✅ **Backend URL:** Set in `fend/src/utils/directionsService.js`
- Default: `http://localhost:8000`

---

## 🚀 Starting the Application

### **Step 1: Start Backend Server**

```bash
cd backend
uvicorn main:app --reload
```

**Backend will run on:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

### **Step 2: Start Frontend Server**

```bash
cd fend
npm run dev
```

**Frontend will run on:** `http://localhost:5173` (or similar Vite port)

---

## 📋 Quick Installation (One Command)

### **Windows (PowerShell)**
```powershell
cd backend; pip install -r requirements.txt; cd ..; cd fend; npm install; cd ..
```

### **Linux/Mac (Bash)**
```bash
cd backend && pip install -r requirements.txt && cd .. && cd fend && npm install && cd ..
```

### **Or Use the Installation Scripts:**
- **Windows:** Run `install-all.bat`
- **Linux/Mac:** Run `chmod +x install-all.sh && ./install-all.sh`

---

## ✅ Verification Checklist

### **Before Starting:**
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL database accessible (Supabase)
- [ ] Firebase project configured
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed

### **After Starting:**
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Can access `http://localhost:8000/docs`
- [ ] Can access `http://localhost:5173`
- [ ] Map loads correctly
- [ ] Location permission works
- [ ] Search functionality works

---

## 🐛 Troubleshooting

### **Backend Issues:**
1. **Database Connection Error:**
   - Check `backend/database.py` for correct database URL
   - Ensure Supabase database is accessible

2. **Port Already in Use:**
   - Change port: `uvicorn main:app --reload --port 8001`

3. **Missing Dependencies:**
   - Reinstall: `pip install -r requirements.txt --upgrade`

### **Frontend Issues:**
1. **Map Not Loading:**
   - Check browser console for errors
   - Ensure Leaflet CSS is loaded
   - Check internet connection (for OpenStreetMap tiles)

2. **Location Permission Denied:**
   - Allow location access in browser settings
   - Use HTTPS or localhost (required for geolocation)

3. **Backend Connection Error:**
   - Check backend is running on port 8000
   - Verify `BACKEND_URL` in `directionsService.js`

---

## 📝 Important Notes

1. **No API Keys Required:**
   - OSRM routing: Free public server
   - Nominatim search: Free public server
   - OpenStreetMap tiles: Free

2. **Database:**
   - PostgreSQL (Supabase) - already configured
   - Tables created automatically on first run

3. **Firebase:**
   - Already configured with credentials
   - Authentication, Firestore, Realtime Database enabled

4. **Location Services:**
   - Requires HTTPS or localhost
   - Browser location permission needed
   - GPS accuracy depends on device

---

## 🎯 Next Steps After Installation

1. **Start Backend:** `cd backend && uvicorn main:app --reload`
2. **Start Frontend:** `cd fend && npm run dev`
3. **Open Browser:** Navigate to `http://localhost:5173`
4. **Test Features:**
   - Allow location access
   - Search for a destination
   - Find routes
   - Test navigation

---

## 📚 Additional Resources

- **Backend API Docs:** `http://localhost:8000/docs`
- **Leaflet Docs:** https://leafletjs.com/
- **React Leaflet Docs:** https://react-leaflet.js.org/
- **OSRM Docs:** http://project-osrm.org/
- **Nominatim Docs:** https://nominatim.org/

---

## ✨ Features Available

- ✅ Live GPS tracking
- ✅ OpenStreetMap integration
- ✅ Route finding with OSRM
- ✅ Place search with Nominatim
- ✅ Safety score calculation
- ✅ Dynamic rerouting
- ✅ Real-time location sharing
- ✅ User authentication
- ✅ Route visualization
- ✅ Turn-by-turn navigation

---

**Happy Coding! 🚀**

