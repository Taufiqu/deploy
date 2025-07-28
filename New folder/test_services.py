# ========================================
# LOCAL DEVELOPMENT TESTING SCRIPT
# ========================================

import requests
import json

# Configuration
FAKTUR_SERVICE_URL = "http://localhost:5001"
BUKTI_SETOR_SERVICE_URL = "http://localhost:5002"

def test_health_checks():
    """Test health check endpoints for both services"""
    print("🔍 Testing Health Checks...")
    
    # Test Faktur Service
    try:
        response = requests.get(f"{FAKTUR_SERVICE_URL}/health")
        print(f"✅ Faktur Service Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Faktur Service Health Check Failed: {e}")
    
    # Test Bukti Setor Service
    try:
        response = requests.get(f"{BUKTI_SETOR_SERVICE_URL}/health")
        print(f"✅ Bukti Setor Service Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Bukti Setor Service Health Check Failed: {e}")

def test_service_info():
    """Test service info endpoints"""
    print("\n📋 Testing Service Info...")
    
    try:
        response = requests.get(f"{BUKTI_SETOR_SERVICE_URL}/api/info")
        print(f"ℹ️ Bukti Setor Service Info: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Service Info Failed: {e}")

def test_endpoints():
    """Test basic endpoints for both services"""
    print("\n🧪 Testing Endpoints...")
    
    # Test Faktur endpoints
    try:
        response = requests.get(f"{FAKTUR_SERVICE_URL}/api/faktur/history/masukan")
        print(f"📊 Faktur History (Masukan): {response.status_code}")
    except Exception as e:
        print(f"❌ Faktur History Test Failed: {e}")
    
    # Test Bukti Setor endpoints
    try:
        response = requests.get(f"{BUKTI_SETOR_SERVICE_URL}/api/bukti-setor/history")
        print(f"📊 Bukti Setor History: {response.status_code}")
    except Exception as e:
        print(f"❌ Bukti Setor History Test Failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Separated OCR Services")
    print("=" * 50)
    
    test_health_checks()
    test_service_info()
    test_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Testing Complete!")
    print("\n📝 Next Steps:")
    print("1. Ensure both services are running locally")
    print("2. Test file upload functionality")
    print("3. Deploy to Railway following RAILWAY_DEPLOYMENT.md")
