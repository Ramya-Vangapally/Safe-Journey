import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth'
import { auth } from '../config/firebase'
import { doc, setDoc, getDoc, updateDoc } from 'firebase/firestore'
import { db } from '../config/firebase'

const backendUrl = "http://localhost:8000" // Your FastAPI backend URL

/**
 * Register a new user with Firebase Auth and create user document in Firestore
 * Also syncs the user to Supabase via backend
 */
export const registerUser = async (userData) => {
  const { fullName, email, phone, password } = userData

  try {
    // Validate inputs
    if (!fullName || !email || !phone || !password) {
      return { success: false, message: 'All fields are required' }
    }

    if (password.length < 6) {
      return { success: false, message: 'Password must be at least 6 characters' }
    }

    // Firebase Auth registration
    const userCredential = await createUserWithEmailAndPassword(auth, email, password)
    const user = userCredential.user

    // Update display name in Firebase
    await updateProfile(user, { displayName: fullName })

    // Generate custom user ID
    const userId = `SJ${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`

    // Firestore document
    const userDoc = {
      id: userId,
      fullName,
      email,
      phone,
      credits: 250000,
      createdAt: new Date().toISOString(),
      lastActiveAt: new Date().toISOString()
    }
    await setDoc(doc(db, 'users', user.uid), userDoc)

    // --- NEW: Sync user to Supabase via backend ---
    try {
      await fetch(`${backendUrl}/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          uid: user.uid,
          email: user.email,
          display_name: fullName,
          phone: phone,
          photo_url: user.photoURL
        })
      })
    } catch (err) {
      console.error('Error syncing to backend:', err)
    }

    return { success: true, user: { uid: user.uid, ...userDoc } }

  } catch (error) {
    let errorMessage = 'Registration failed. Please try again.'

    if (error.code === 'auth/email-already-in-use') {
      errorMessage = 'User with this email already exists'
    } else if (error.code === 'auth/invalid-email') {
      errorMessage = 'Invalid email address'
    } else if (error.code === 'auth/weak-password') {
      errorMessage = 'Password is too weak'
    }

    return { success: false, message: errorMessage }
  }
}

/**
 * Login user with Firebase Auth
 * Also updates lastActiveAt and syncs to Supabase backend
 */
export const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password)
    const user = userCredential.user

    // Fetch Firestore user document
    const userDocRef = doc(db, 'users', user.uid)
    const userDocSnap = await getDoc(userDocRef)

    if (userDocSnap.exists()) {
      // Update last active timestamp in Firestore
      await updateDoc(userDocRef, { lastActiveAt: new Date().toISOString() })

      // --- NEW: Sync user to Supabase backend ---
      try {
        await fetch(`${backendUrl}/users/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            uid: user.uid,
            email: user.email,
            display_name: user.displayName,
            phone: userDocSnap.data().phone,
            photo_url: user.photoURL
          })
        })
      } catch (err) {
        console.error('Error syncing to backend:', err)
      }

      return { success: true, user: { uid: user.uid, ...userDocSnap.data() } }
    } else {
      return { success: false, message: 'User profile not found' }
    }

  } catch (error) {
    let errorMessage = 'Invalid email or password'

    if (error.code === 'auth/user-not-found') errorMessage = 'No account found with this email'
    else if (error.code === 'auth/wrong-password') errorMessage = 'Incorrect password'
    else if (error.code === 'auth/invalid-email') errorMessage = 'Invalid email address'

    return { success: false, message: errorMessage }
  }
}

/**
 * Logout user
 */
export const logoutUser = async () => {
  try {
    await signOut(auth)
    return { success: true }
  } catch (error) {
    return { success: false, message: error.message }
  }
}

/**
 * Get current authenticated user
 */
export const getCurrentUser = async () => {
  return new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      unsubscribe()

      if (!firebaseUser) {
        resolve(null)
        return
      }

      try {
        const userDoc = await getDoc(doc(db, 'users', firebaseUser.uid))
        if (userDoc.exists()) {
          resolve({ uid: firebaseUser.uid, ...userDoc.data() })
        } else {
          resolve(null)
        }
      } catch (error) {
        console.error('Error fetching user data:', error)
        resolve(null)
      }
    })
  })
}

/**
 * Update user credits in Firestore
 */
export const updateUserCredits = async (userId, newCredits) => {
  try {
    await updateDoc(doc(db, 'users', userId), { credits: newCredits })
    return { success: true }
  } catch (error) {
    console.error('Error updating credits:', error)
    return { success: false, message: error.message }
  }
}
