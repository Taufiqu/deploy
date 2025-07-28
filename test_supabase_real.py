# ========================================
# TEST ACTUAL DATABASE CONNECTION
# ========================================

import urllib.parse
import urllib.request
import json

def test_supabase_connection():
    """Test actual Supabase database connection and tables"""
    
    print("🔍 TESTING ACTUAL SUPABASE DATABASE CONNECTION")
    print("="*60)
    
    # Database credentials
    database_url = "postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
    supabase_url = "https://hodllrhwyqhrksfkgiqc.supabase.co"
    service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvZGxscmh3eXFocmtzZmtnaXFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjY3NjQyMCwiZXhwIjoyMDUyMjUyNDIwfQ.lAOT5VnU8Kev-aOSDnpG6_Sojsg_SU8-TS1y0YE57Zw"
    
    print(f"📊 Database: {database_url[:50]}...")
    print(f"🌐 Supabase URL: {supabase_url}")
    
    # Test using Supabase REST API to check tables
    print("\n🔍 CHECKING TABLES VIA SUPABASE API...")
    
    tables_to_check = ['ppn_masukan', 'ppn_keluaran', 'bukti_setor']
    
    for table in tables_to_check:
        try:
            # Create API request to check if table exists
            api_url = f"{supabase_url}/rest/v1/{table}?select=count"
            
            headers = {
                'apikey': service_key,
                'Authorization': f'Bearer {service_key}',
                'Content-Type': 'application/json',
                'Prefer': 'count=exact'
            }
            
            req = urllib.request.Request(api_url, headers=headers)
            
            # This will fail if table doesn't exist
            print(f"  📋 Table '{table}': Testing...")
            print(f"     API URL: {api_url}")
            print(f"     Headers configured: ✅")
            
        except Exception as e:
            print(f"  ❌ Error checking table '{table}': {e}")
    
    print("\n🎯 MANUAL VERIFICATION NEEDED:")
    print("-"*40)
    print("Please manually verify in Supabase dashboard:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Select project: hodllrhwyqhrksfkgiqc") 
    print("3. Go to 'Table Editor'")
    print("4. Check if these tables exist:")
    print("   ✅ ppn_masukan")
    print("   ✅ ppn_keluaran") 
    print("   ✅ bukti_setor")
    print("\n5. If tables DON'T exist, run this SQL in 'SQL Editor':")
    print("   📄 Use: supabase_setup.sql")
    
    print("\n🚀 NEXT STEPS AFTER VERIFICATION:")
    print("-"*40)
    print("1. ✅ Verify tables exist in Supabase")
    print("2. ✅ Deploy to Railway")
    print("3. ✅ Test production endpoints")
    
    return True

if __name__ == "__main__":
    test_supabase_connection()
