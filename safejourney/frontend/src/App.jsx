import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from './config/firebase'
import { getCurrentUser } from './utils/firebaseAuth'
import AuthPage from './components/AuthPage'
import PreferencesPage from './components/PreferencesPage'
import JourneyPlanner from './components/JourneyPlanner'
import SingleRouteView from './components/SingleRouteView'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const [preferencesCompleted, setPreferencesCompleted] = useState(false)

  useEffect(() => {
    // Listen to Firebase auth state changes
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        // Verify user data exists in Firestore
        const user = await getCurrentUser()
        setIsAuthenticated(!!user)
        // Check if preferences were completed in this session
        const prefs = sessionStorage.getItem('preferencesCompleted')
        setPreferencesCompleted(!!prefs)
      } else {
        setIsAuthenticated(false)
        setPreferencesCompleted(false)
      }
      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-dark-bg">
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={
            isAuthenticated ? <Navigate to={preferencesCompleted ? "/journey-planner" : "/preferences"} /> : <Navigate to="/login" />
          } 
        />
        <Route 
          path="/login" 
          element={
            isAuthenticated ? <Navigate to="/preferences" /> : <AuthPage setIsAuthenticated={setIsAuthenticated} />
          } 
        />
        <Route 
          path="/preferences" 
          element={
            isAuthenticated ? (
              <PreferencesPage onComplete={() => {
                sessionStorage.setItem('preferencesCompleted', 'true')
                setPreferencesCompleted(true)
              }} />
            ) : <Navigate to="/login" />
          } 
        />
        <Route 
          path="/journey-planner" 
          element={
            isAuthenticated ? <JourneyPlanner /> : <Navigate to="/login" />
          } 
        />
        <Route 
          path="/journey" 
          element={
            isAuthenticated ? <JourneyPlanner /> : <Navigate to="/login" />
          } 
        />
        <Route 
          path="/route/:routeId" 
          element={
            isAuthenticated ? <SingleRouteView /> : <Navigate to="/login" />
          } 
        />
      </Routes>
    </Router>
  )
}

export default App

