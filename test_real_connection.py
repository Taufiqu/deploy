# ========================================
# REAL DATABASE CONNECTION TEST
# ========================================

import os
import sys
from pathlib import Path

# Add the service directories to Python path
sys.path.append(str(Path("faktur-service")))
sys.path.append(str(Path("bukti-setor-service")))

def test_database_connection_real():
    """Test real database connection with actual credentials"""
    
    print("🔍 TESTING REAL DATABASE CONNECTION")
    print("="*60)
    
    # Set environment variables
    os.environ['DATABASE_URL'] = "postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
    os.environ['SUPABASE_URL'] = "https://hodllrhwyqhrksfkgiqc.supabase.co"
    os.environ['FLASK_ENV'] = "development"
    os.environ['SECRET_KEY'] = "test-secret-key"
    
    try:
        # Test importing and basic setup
        print("📦 Testing imports...")
        
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        print("  ✅ Flask and SQLAlchemy imported successfully")
        
        # Create test app
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        
        db = SQLAlchemy(app)
        print("  ✅ Flask app and SQLAlchemy configured")
        
        # Test database connection
        with app.app_context():
            print("\n🔗 Testing database connection...")
            
            # Try to execute a simple query
            result = db.session.execute(db.text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("  ✅ Database connection successful!")
                
                # Test table existence
                print("\n📊 Checking tables...")
                
                tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('ppn_masukan', 'ppn_keluaran', 'bukti_setor')
                ORDER BY table_name;
                """
                
                result = db.session.execute(db.text(tables_query))
                tables = [row[0] for row in result.fetchall()]
                
                expected_tables = ['bukti_setor', 'ppn_keluaran', 'ppn_masukan']
                
                for table in expected_tables:
                    if table in tables:
                        print(f"  ✅ Table '{table}' exists")
                        
                        # Count records in each table
                        count_query = f"SELECT COUNT(*) FROM {table}"
                        count_result = db.session.execute(db.text(count_query))
                        count = count_result.fetchone()[0]
                        print(f"     Records: {count}")
                    else:
                        print(f"  ❌ Table '{table}' missing")
                
                if len(tables) == 3:
                    print("\n🎉 ALL TABLES EXIST AND ACCESSIBLE!")
                    print("✅ Database is ready for Railway deployment")
                    return True
                else:
                    print(f"\n❌ Missing tables. Found: {tables}")
                    return False
            else:
                print("  ❌ Database connection test failed")
                return False
                
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        print("  💡 Try: pip install Flask Flask-SQLAlchemy psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"  ❌ Database connection error: {e}")
        print("  💡 Check if Supabase database is accessible")
        return False

def test_both_services_config():
    """Test if both service configurations would work"""
    
    print("\n" + "="*60)
    print("🧾 TESTING SERVICE CONFIGURATIONS")
    print("="*60)
    
    # Check if service files exist
    faktur_files = [
        "faktur-service/app_faktur.py",
        "faktur-service/models.py",
        "faktur-service/config.py",
        "faktur-service/Dockerfile.faktur"
    ]
    
    bukti_setor_files = [
        "bukti-setor-service/app_bukti_setor.py", 
        "bukti-setor-service/models.py",
        "bukti-setor-service/config.py",
        "bukti-setor-service/Dockerfile.bukti-setor"
    ]
    
    print("📁 Faktur Service Files:")
    for file in faktur_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
    
    print("\n📁 Bukti Setor Service Files:")
    for file in bukti_setor_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
    
    # Check if all required files exist
    all_files = faktur_files + bukti_setor_files
    missing_files = [f for f in all_files if not Path(f).exists()]
    
    if not missing_files:
        print("\n✅ All service files exist and ready for deployment!")
        return True
    else:
        print(f"\n❌ Missing files: {missing_files}")
        return False

def main():
    """Main test function"""
    print("🧪 COMPREHENSIVE DATABASE & SERVICE TEST")
    print("="*70)
    
    # Test database connection
    db_ok = test_database_connection_real()
    
    # Test service configurations
    services_ok = test_both_services_config()
    
    print("\n" + "="*70)
    print("🎯 FINAL DEPLOYMENT STATUS:")
    print("="*70)
    
    print(f"🗄️  Database Connection: {'✅ Ready' if db_ok else '❌ Failed'}")
    print(f"🧾 Service Files: {'✅ Ready' if services_ok else '❌ Missing Files'}")
    
    if db_ok and services_ok:
        print("\n🚀 🎉 EVERYTHING IS READY FOR RAILWAY DEPLOYMENT! 🎉 🚀")
        print("\n📋 Next Steps:")
        print("1. Go to Railway.app")
        print("2. Deploy Faktur Service (Root: faktur-service)")
        print("3. Deploy Bukti Setor Service (Root: bukti-setor-service)")
        print("4. Use environment variables from railway_env_*.txt files")
        print("5. Test deployed services")
    else:
        print("\n❌ DEPLOYMENT NOT READY - Fix issues above first")
    
    print("="*70)

if __name__ == "__main__":
    main()
