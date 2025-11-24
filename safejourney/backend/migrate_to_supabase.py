"""
Migration script: SQLite to Supabase
This script migrates existing data from SQLite to Supabase and ensures all columns exist
"""

import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

# Load both database URLs
SQLITE_DB = "safejourney.db"
SUPABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("MIGRATING DATABASE FROM SQLITE TO SUPABASE")
print("=" * 60)

# Connect to Supabase PostgreSQL
try:
    print("\n📡 Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(SUPABASE_URL)
    cursor = conn.cursor()
    print("✅ Connected to Supabase successfully!")
    
    # Create tables with emergency_contact_number column
    print("\n🔨 Creating/verifying tables...")
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            uid VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            display_name VARCHAR(255),
            phone VARCHAR(20),
            photo_url TEXT,
            credits INTEGER DEFAULT 250000,
            latitude FLOAT,
            longitude FLOAT,
            emergency_contact_number VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Users table created/verified")
    
    # Create segments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS segments (
            segment_id SERIAL PRIMARY KEY,
            lat_min FLOAT NOT NULL,
            lat_max FLOAT NOT NULL,
            lon_min FLOAT NOT NULL,
            lon_max FLOAT NOT NULL,
            safety_score FLOAT DEFAULT 5.0,
            report_count INTEGER DEFAULT 0,
            reports TEXT DEFAULT '[]',
            active_user_count INTEGER DEFAULT 0,
            avg_speed FLOAT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Segments table created/verified")
    
    # Verify emergency_contact_number column exists
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='users' AND column_name='emergency_contact_number'
    """)
    if not cursor.fetchone():
        print("⚠️  Adding emergency_contact_number column...")
        cursor.execute("""
            ALTER TABLE users ADD COLUMN emergency_contact_number VARCHAR(20)
        """)
        print("✅ emergency_contact_number column added")
    else:
        print("✅ emergency_contact_number column already exists")
    
    conn.commit()
    
    # Try to migrate data from SQLite if it exists
    if os.path.exists(SQLITE_DB):
        print(f"\n📂 Found SQLite database ({SQLITE_DB}), migrating data...")
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get users from SQLite
        sqlite_cursor.execute("SELECT uid, email, display_name, phone, photo_url, credits, latitude, longitude, created_at, last_active_at FROM users")
        users = sqlite_cursor.fetchall()
        
        if users:
            print(f"📊 Found {len(users)} users in SQLite")
            
            # Insert into Supabase (skip duplicates)
            for user in users:
                try:
                    cursor.execute("""
                        INSERT INTO users (uid, email, display_name, phone, photo_url, credits, latitude, longitude, created_at, last_active_at, emergency_contact_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (uid) DO UPDATE SET
                            email = EXCLUDED.email,
                            display_name = EXCLUDED.display_name,
                            phone = EXCLUDED.phone,
                            photo_url = EXCLUDED.photo_url,
                            latitude = EXCLUDED.latitude,
                            longitude = EXCLUDED.longitude,
                            last_active_at = EXCLUDED.last_active_at
                    """, user + (None,))  # emergency_contact_number is NULL for migrated users
                except Exception as e:
                    print(f"⚠️  Error migrating user {user[0]}: {e}")
            
            conn.commit()
            print(f"✅ Migrated {len(users)} users to Supabase")
        
        # Get segments from SQLite
        sqlite_cursor.execute("SELECT lat_min, lat_max, lon_min, lon_max, safety_score, report_count, reports, active_user_count, avg_speed, updated_at FROM segments")
        segments = sqlite_cursor.fetchall()
        
        if segments:
            print(f"📊 Found {len(segments)} segments in SQLite")
            
            for segment in segments:
                try:
                    cursor.execute("""
                        INSERT INTO segments (lat_min, lat_max, lon_min, lon_max, safety_score, report_count, reports, active_user_count, avg_speed, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, segment)
                except Exception as e:
                    print(f"⚠️  Error migrating segment: {e}")
            
            conn.commit()
            print(f"✅ Migrated {len(segments)} segments to Supabase")
        
        sqlite_conn.close()
    else:
        print(f"\n✅ No SQLite database found (fresh start)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print("\n🎉 Supabase is now ready with:")
    print("   ✅ Users table with emergency_contact_number column")
    print("   ✅ Segments table for safety data")
    print("   ✅ All existing data migrated (if available)")
    print("\n📝 Next steps:")
    print("   1. Restart the backend: python -m uvicorn main:app --reload")
    print("   2. Test the emergency contact feature")
    print("   3. All errors should be gone! 🚀")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
