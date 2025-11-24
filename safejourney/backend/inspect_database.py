"""
Database Inspector - View tables schema and data in SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "safejourney.db"

def inspect_database():
    """Inspect SQLite database schema and data"""
    
    # Check if database exists
    if not Path(DB_PATH).exists():
        print(f"❌ Database file not found: {DB_PATH}")
        print("   Run backend first to create database")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("=" * 80)
        print("DATABASE INSPECTOR - SafeJourney SQLite Database")
        print("=" * 80)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("\n❌ No tables found in database")
            conn.close()
            return
        
        print(f"\n✅ Found {len(tables)} table(s):\n")
        
        for table_name in tables:
            table = table_name[0]
            
            print("\n" + "=" * 80)
            print(f"📊 TABLE: {table.upper()}")
            print("=" * 80)
            
            # Get table schema
            print("\n📋 Schema:")
            print("-" * 80)
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            for col_id, col_name, col_type, not_null, default, pk in columns:
                nullable = "NOT NULL" if not_null else "NULL"
                primary = "PRIMARY KEY" if pk else ""
                print(f"  • {col_name:25} {col_type:15} {nullable:10} {primary}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            
            print(f"\n📈 Data Count: {row_count} row(s)")
            
            if row_count > 0:
                # Get all data
                print("\n📄 Data:")
                print("-" * 80)
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                # Get column names
                col_names = [description[0] for description in cursor.description]
                
                # Display data
                for i, row in enumerate(rows, 1):
                    print(f"\n  Record {i}:")
                    for col_name, value in zip(col_names, row):
                        # Format value for display
                        if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                            try:
                                formatted_value = json.loads(value)
                                print(f"    {col_name}: {json.dumps(formatted_value, indent=6)}")
                            except:
                                print(f"    {col_name}: {value}")
                        else:
                            print(f"    {col_name}: {value}")
            
            print()
        
        # Database statistics
        print("\n" + "=" * 80)
        print("DATABASE STATISTICS")
        print("=" * 80)
        
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();")
        db_size = cursor.fetchone()[0]
        print(f"\n💾 Database Size: {db_size / 1024:.2f} KB")
        print(f"📍 Database Path: {DB_PATH}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_database()
