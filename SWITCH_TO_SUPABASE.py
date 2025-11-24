"""
SWITCH TO SUPABASE - Configuration Helper
============================================

To switch from SQLite to Supabase, you need:

1. SUPABASE PROJECT URL (from Supabase dashboard)
2. SUPABASE DATABASE PASSWORD (created during setup)

Steps to Get Your Connection String:
====================================

1. Go to: https://app.supabase.com/
2. Select your project
3. Click "Database" in left sidebar
4. Click "Connection String" tab
5. Select "URI" tab (not Parameters)
6. Choose "Python"
7. Copy the connection string
8. Replace [YOUR-PASSWORD] with your actual password

The URI will look like:
postgresql://postgres:[YOUR-PASSWORD]@db.XXXXXX.supabase.co:5432/postgres

Full example:
postgresql://postgres:mypassword123@db.abc123xyz.supabase.co:5432/postgres
"""

import os
from pathlib import Path

# Ask user for Supabase connection string
print("\n" + "="*80)
print("SWITCH DATABASE TO SUPABASE")
print("="*80)

print(__doc__)

print("\n" + "="*80)
print("WHAT TO DO:")
print("="*80)
print("""
1. Copy your Supabase connection string from the Supabase dashboard
2. Make sure it includes the password (replace [YOUR-PASSWORD])
3. Paste it below

Example format:
postgresql://postgres:PASSWORD@db.XXXXX.supabase.co:5432/postgres
""")

# Get user input
connection_string = input("\nEnter your Supabase PostgreSQL connection string:\n> ").strip()

if not connection_string:
    print("❌ No connection string provided")
    exit(1)

if "postgresql://" not in connection_string:
    print("❌ Invalid format. Must start with 'postgresql://'")
    exit(1)

# Update .env file
env_file = Path("safejourney/backend/.env")

# Read current .env
content = env_file.read_text()

# Replace DATABASE_URL
new_content = content.replace(
    'DATABASE_URL=sqlite:///./safejourney.db',
    f'DATABASE_URL={connection_string}'
)

# Write back
env_file.write_text(new_content)

print("\n" + "="*80)
print("✅ CONFIGURATION UPDATED")
print("="*80)
print(f"""
Database URL updated in .env file

NEW CONFIGURATION:
{connection_string[:50]}...{connection_string[-20:]}

NEXT STEPS:
1. Start the backend: python -m uvicorn main:app --reload
2. Tables will be created automatically
3. Database is now using Supabase ✅

NOTE:
- Make sure Supabase maintenance is complete
- Check https://status.supabase.com for status
- If connection fails, verify:
  ✓ Connection string is correct
  ✓ Password is correct
  ✓ Your IP is allowed (check firewall)
  ✓ Supabase project is not paused
""")
