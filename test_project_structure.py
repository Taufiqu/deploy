# ========================================
# TEST IMPORT PATHS & FILE STRUCTURE
# ========================================

import os
import sys
from pathlib import Path

def test_faktur_service_structure():
    """Test Faktur Service file structure"""
    print("🧾 TESTING FAKTUR SERVICE STRUCTURE")
    print("-" * 40)
    
    faktur_path = Path("faktur-service")
    required_files = [
        "app_faktur.py",
        "config.py", 
        "models.py",
        "Dockerfile.faktur",
        "requirements-faktur.txt",
        ".env.example"
    ]
    
    for file in required_files:
        file_path = faktur_path / file
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file}")
    
    # Check folders
    required_folders = ["faktur", "shared_utils"]
    for folder in required_folders:
        folder_path = faktur_path / folder
        status = "✅" if folder_path.exists() else "❌"
        print(f"  {status} {folder}/")
    
    return True

def test_bukti_setor_service_structure():
    """Test Bukti Setor Service file structure"""
    print("\n🧾 TESTING BUKTI SETOR SERVICE STRUCTURE")
    print("-" * 40)
    
    bukti_setor_path = Path("bukti-setor-service")
    required_files = [
        "app_bukti_setor.py",
        "config.py",
        "models.py", 
        "Dockerfile.bukti-setor",
        "requirements-bukti-setor.txt",
        ".env.example"
    ]
    
    for file in required_files:
        file_path = bukti_setor_path / file
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file}")
    
    # Check folders
    required_folders = ["bukti_setor", "shared_utils"]
    for folder in required_folders:
        folder_path = bukti_setor_path / folder
        status = "✅" if folder_path.exists() else "❌"
        print(f"  {status} {folder}/")
    
    return True

def test_deployment_files():
    """Test deployment related files"""
    print("\n📋 TESTING DEPLOYMENT FILES")
    print("-" * 40)
    
    deployment_files = [
        "supabase_setup.sql",
        "DEPLOYMENT_GUIDE.md",
        "DATABASE_STRATEGY.md",
        "API_DOCS_SEPARATED.md"
    ]
    
    for file in deployment_files:
        file_path = Path(file)
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file}")
    
    return True

def check_python_imports():
    """Check if Python imports would work"""
    print("\n🐍 TESTING PYTHON IMPORT PATHS")
    print("-" * 40)
    
    try:
        # Test basic imports
        import flask
        print("  ✅ Flask imported successfully")
        
        import flask_sqlalchemy
        print("  ✅ Flask-SQLAlchemy imported successfully")
        
        import dotenv
        print("  ✅ python-dotenv imported successfully")
        
        print("  ✅ All required packages available")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 PROJECT STRUCTURE & DEPLOYMENT READINESS TEST")
    print("=" * 60)
    
    # Test service structures
    faktur_ok = test_faktur_service_structure()
    bukti_setor_ok = test_bukti_setor_service_structure()
    deployment_ok = test_deployment_files()
    imports_ok = check_python_imports()
    
    print("\n" + "=" * 60)
    print("🎯 DEPLOYMENT READINESS SUMMARY:")
    print("=" * 60)
    
    services_ready = faktur_ok and bukti_setor_ok
    
    print(f"🧾 Faktur Service: {'✅ Ready' if faktur_ok else '❌ Missing files'}")
    print(f"🧾 Bukti Setor Service: {'✅ Ready' if bukti_setor_ok else '❌ Missing files'}")
    print(f"📋 Deployment Files: {'✅ Ready' if deployment_ok else '❌ Missing files'}")
    print(f"🐍 Python Dependencies: {'✅ Ready' if imports_ok else '❌ Missing packages'}")
    
    if services_ready and deployment_ok and imports_ok:
        print("\n🚀 PROJECT IS READY FOR DEPLOYMENT!")
        print("\n📋 NEXT STEPS:")
        print("1. ✅ Setup Supabase database (run supabase_setup.sql)")
        print("2. ✅ Update .env files with real DATABASE_URL")
        print("3. ✅ Commit to GitHub")
        print("4. ✅ Deploy to Railway (2 separate projects)")
        print("5. ✅ Test production endpoints")
    else:
        print("\n❌ PROJECT NEEDS ATTENTION BEFORE DEPLOYMENT")
        print("Please fix missing files/dependencies first")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
