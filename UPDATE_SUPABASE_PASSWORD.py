#!/usr/bin/env python3
"""
UPDATE SUPABASE PASSWORD IN .env
=================================
"""

from pathlib import Path

print("\n" + "="*80)
print("UPDATE SUPABASE PASSWORD")
print("="*80)
print("""
Your .env file currently has:
DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.rskqbrxwwqyluxbzuocg.supabase.co:5432/postgres

The [YOUR_PASSWORD] is a PLACEHOLDER and needs to be replaced with your actual password.

Where to find your Supabase password:
1. Go to https://app.supabase.com
2. Click on your project
3. Click "Database" in left sidebar
4. Look for the password you set when creating the project
5. If you forgot it, you can reset it in the Database settings

""")

password = input("Enter your actual Supabase database password:\n> ").strip()

if not password:
    print("❌ No password provided")
    exit(1)

# Update .env file
env_file = Path("safejourney/backend/.env")

# Read current .env
content = env_file.read_text()

# Replace the placeholder
new_content = content.replace(
    'DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@',
    f'DATABASE_URL=postgresql://postgres:{password}@'
)

# Write back
env_file.write_text(new_content)

print("\n" + "="*80)
print("✅ PASSWORD UPDATED IN .env")
print("="*80)
print("""
Your Supabase connection is now ready!

NEXT STEP:
Start the backend again:
  python -m uvicorn main:app --reload

You should see:
  ✅ Database tables initialized successfully
  INFO: Uvicorn running on http://127.0.0.1:8000
""")
