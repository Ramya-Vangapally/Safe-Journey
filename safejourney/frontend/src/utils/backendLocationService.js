const BACKEND_URL = 'http://localhost:8000'

/**
 * Update user location in PostgreSQL via backend
 */
export const updateUserLocationInDB = async (uid, location) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/update-location`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        uid: uid,
        latitude: location.lat,
        longitude: location.lng
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to update location')
    }

    const data = await response.json()
    console.log('✅ Location updated in PostgreSQL:', data)
    return data
  } catch (error) {
    console.error('❌ Error updating location in backend:', error)
    throw error
  }
}

/**
 * Get user's last known location from PostgreSQL
 */
export const getUserLocationFromDB = async (uid) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/user-location/${uid}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        console.log('📍 User location not found in database')
        return null
      }
      throw new Error('Failed to fetch user location')
    }

    const data = await response.json()
    if (data.success && data.location) {
      console.log('✅ Fetched user location from PostgreSQL:', data.location)
      return {
        lat: data.location.latitude,
        lng: data.location.longitude
      }
    }
    return null
  } catch (error) {
    console.error('❌ Error fetching user location from database:', error)
    return null
  }
}

/**
 * Get active users from PostgreSQL
 */
export const getActiveUsersFromDB = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/active-users`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch active users')
    }

    const data = await response.json()
    console.log(`📍 Fetched ${data.count} active users from PostgreSQL`)
    return data.users
  } catch (error) {
    console.error('❌ Error fetching active users:', error)
    return []
  }
}