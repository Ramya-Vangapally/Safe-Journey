"""
Database Schema Modifier - Redesign tables and add data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "safejourney.db"

# ==================== SCHEMA DEFINITIONS ====================

USERS_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    display_name VARCHAR,
    phone VARCHAR,
    photo_url VARCHAR,
    credits INTEGER NOT NULL DEFAULT 250000,
    latitude FLOAT,
    longitude FLOAT,
    emergency_contact_number VARCHAR,
    created_at DATETIME NOT NULL,
    last_active_at DATETIME NOT NULL
)
"""

# ==================== CUSTOM SEGMENT SCHEMA ====================
# MODIFY THIS BASED ON YOUR REQUIREMENTS
SEGMENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS segments (
    segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    region VARCHAR NOT NULL,
    lat_min FLOAT NOT NULL,
    lat_max FLOAT NOT NULL,
    lon_min FLOAT NOT NULL,
    lon_max FLOAT NOT NULL,
    safety_score FLOAT DEFAULT 5.0,
    description VARCHAR,
    population INTEGER,
    lighting_quality VARCHAR,
    traffic_density VARCHAR,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
"""

# ==================== SAMPLE DATA ====================

SAMPLE_SEGMENTS = [
    {
        "name": "Downtown Central",
        "region": "Hyderabad",
        "lat_min": 17.36,
        "lat_max": 17.38,
        "lon_min": 78.47,
        "lon_max": 78.49,
        "safety_score": 4.5,
        "description": "City center, busy commercial area",
        "population": 50000,
        "lighting_quality": "Excellent",
        "traffic_density": "High"
    },
    {
        "name": "Tech Park Zone",
        "region": "Hyderabad",
        "lat_min": 17.45,
        "lat_max": 17.47,
        "lon_min": 78.37,
        "lon_max": 78.39,
        "safety_score": 4.8,
        "description": "IT hub with modern infrastructure",
        "population": 30000,
        "lighting_quality": "Excellent",
        "traffic_density": "Medium"
    },
    {
        "name": "Residential Area A",
        "region": "Hyderabad",
        "lat_min": 17.40,
        "lat_max": 17.42,
        "lon_min": 78.40,
        "lon_max": 78.42,
        "safety_score": 3.5,
        "description": "Residential colony with mixed safety",
        "population": 20000,
        "lighting_quality": "Poor",
        "traffic_density": "Low"
    }
]

# ==================== FUNCTIONS ====================

def backup_database():
    """Backup existing database"""
    if Path(DB_PATH).exists():
        import shutil
        backup_path = DB_PATH.replace(".db", "_backup.db")
        shutil.copy(DB_PATH, backup_path)
        print(f"✅ Backed up database to: {backup_path}")
        return backup_path
    return None

def recreate_database(new_schema=None):
    """Drop and recreate tables with new schema"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n🔄 Recreating database schema...\n")
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS segments")
        cursor.execute("DROP TABLE IF EXISTS users")
        print("✅ Dropped old tables")
        
        # Create users table (keep existing)
        cursor.execute(USERS_SCHEMA)
        print("✅ Created USERS table")
        
        # Create segments table with new or custom schema
        if new_schema:
            cursor.execute(new_schema)
            print("✅ Created SEGMENTS table (custom schema)")
        else:
            cursor.execute(SEGMENTS_SCHEMA)
            print("✅ Created SEGMENTS table (default schema)")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Schema recreation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def add_sample_data():
    """Add sample segment data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n📥 Adding sample data...\n")
        
        for segment in SAMPLE_SEGMENTS:
            cursor.execute("""
                INSERT INTO segments 
                (name, region, lat_min, lat_max, lon_min, lon_max, 
                 safety_score, description, population, lighting_quality, traffic_density, 
                 created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                segment["name"],
                segment["region"],
                segment["lat_min"],
                segment["lat_max"],
                segment["lon_min"],
                segment["lon_max"],
                segment["safety_score"],
                segment["description"],
                segment["population"],
                segment["lighting_quality"],
                segment["traffic_density"],
                datetime.now(),
                datetime.now()
            ))
            print(f"  ✅ Added: {segment['name']} ({segment['region']})")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Sample data added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding data: {e}")
        return False

def add_custom_data(data_list):
    """Add custom segment data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n📥 Adding custom data...\n")
        
        for segment in data_list:
            cursor.execute("""
                INSERT INTO segments 
                (name, region, lat_min, lat_max, lon_min, lon_max, 
                 safety_score, description, population, lighting_quality, traffic_density, 
                 created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                segment.get("name", "Unknown"),
                segment.get("region", "Unknown"),
                segment.get("lat_min", 0),
                segment.get("lat_max", 0),
                segment.get("lon_min", 0),
                segment.get("lon_max", 0),
                segment.get("safety_score", 5.0),
                segment.get("description", ""),
                segment.get("population", 0),
                segment.get("lighting_quality", "Unknown"),
                segment.get("traffic_density", "Unknown"),
                datetime.now(),
                datetime.now()
            ))
            print(f"  ✅ Added: {segment.get('name')}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Custom data added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding data: {e}")
        return False

def view_schema():
    """View current schema"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n" + "=" * 80)
        print("CURRENT SCHEMA")
        print("=" * 80)
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n📊 TABLE: {table_name.upper()}")
            print("-" * 80)
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                print(f"  {col_name:25} {col_type:15}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DATABASE SCHEMA MODIFIER")
    print("=" * 80)
    
    # Step 1: Backup
    backup_database()
    
    # Step 2: Recreate schema
    recreate_database()
    
    # Step 3: Add sample data
    add_sample_data()
    
    # Step 4: View schema
    view_schema()
    
    print("\n" + "=" * 80)
    print("✅ Database modification complete!")
    print("=" * 80)
