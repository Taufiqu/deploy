# ========================================
# SIMPLE SUPABASE CONNECTION TEST
# ========================================

import os
from dotenv import load_dotenv
import urllib.parse as urlparse

# Load environment variables
load_dotenv('.env.local')

print("🚀 TESTING SUPABASE CONNECTION...")
print("=" * 50)

# Get database URL
database_url = os.getenv('DATABASE_URL')
print(f"📊 DATABASE_URL loaded: {database_url[:50]}..." if database_url else "❌ DATABASE_URL not found")

if database_url:
    # Parse URL to check components
    parsed = urlparse.urlparse(database_url)
    print(f"🔗 Host: {parsed.hostname}")
    print(f"🔗 Port: {parsed.port}")
    print(f"🔗 Database: {parsed.path[1:]}")  # Remove leading slash
    print(f"🔗 Username: {parsed.username}")

# Test using simple connection method
try:
    import psycopg2
    print("\n✅ psycopg2 is available")
    
    # Test connection
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Test query
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Database connection successful!")
    print(f"📊 PostgreSQL version: {version[0]}")
    
    # Test table check
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"📋 Existing tables: {[table[0] for table in tables]}")
    
    # Close connections
    cursor.close()
    conn.close()
    print("✅ Connection closed successfully")
    
except ImportError:
    print("❌ psycopg2 not available - need to install database drivers")
    print("💡 Try: pip install psycopg2-binary")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("🔍 Check your DATABASE_URL and internet connection")

print("\n" + "=" * 50)
print("🏁 Test completed!")
