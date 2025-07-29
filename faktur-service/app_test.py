# ========================================
# FAKTUR SERVICE - MINIMAL FOR TESTING
# ========================================

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

print("🚀 STARTING MINIMAL FAKTUR SERVICE...")
print(f"📊 Python version: {sys.version}")
print(f"📊 PORT environment: {os.environ.get('PORT', 'NOT SET')}")

# Create Flask app
app = Flask(__name__)

# Enable CORS for all domains and all routes
CORS(app, 
     origins=["*"],  # Allow all origins for now
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False)

# Basic config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-secret-key')

print("✅ Flask app with CORS created successfully")

@app.route('/', methods=['GET'])
def home():
    print("📝 Home endpoint called")
    return jsonify({
        "service": "faktur-minimal",
        "status": "running",
        "message": "Deployment test successful!",
        "timestamp": str(datetime.utcnow())
    })

@app.route('/health', methods=['GET'])
def health():
    print("🏥 Health endpoint called")
    return jsonify({
        "status": "healthy",
        "service": "faktur-minimal", 
        "version": "1.0.0"
    })

@app.route('/test', methods=['GET'])
def test():
    print("🧪 Test endpoint called")
    return jsonify({
        "database": "not connected (test mode)",
        "ocr": "disabled (test mode)",
        "environment": {
            "PORT": os.environ.get('PORT', 'not set'),
            "FLASK_ENV": os.environ.get('FLASK_ENV', 'not set')
        }
    })

# API ENDPOINTS FOR FAKTUR PROCESSING
@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_invoice():
    print("📄 Process invoice endpoint called")
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        # For now, return a mock response since we don't have OCR yet
        return jsonify({
            "status": "success",
            "message": "Invoice processing endpoint working (OCR disabled in minimal mode)",
            "data": {
                "processed": True,
                "ocr_engine": "tesseract (disabled)",
                "filename": "test.pdf",
                "extracted_data": {
                    "supplier": "Test Supplier",
                    "invoice_number": "INV-2025-001", 
                    "amount": 1000000,
                    "tax": 110000,
                    "note": "This is a mock response - OCR will be added later"
                }
            },
            "timestamp": str(datetime.utcnow())
        }), 200
        
    except Exception as e:
        print(f"❌ Error in process_invoice: {e}")
        return jsonify({
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }), 500

print("✅ All routes registered with CORS support")

if __name__ == '__main__':
    # Railway automatically sets PORT environment variable
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
