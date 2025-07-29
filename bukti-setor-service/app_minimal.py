# ========================================
# MINIMAL BUKTI SETOR APP WITH CORS & API ENDPOINTS
# ========================================

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

print("🚀 STARTING MINIMAL BUKTI SETOR APP WITH CORS...")
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
        "service": "bukti-setor-minimal",
        "status": "running",
        "message": "Bukti Setor deployment test successful!",
        "timestamp": str(datetime.utcnow())
    })

@app.route('/health', methods=['GET'])
def health():
    print("🏥 Health endpoint called")
    return jsonify({
        "status": "healthy",
        "service": "bukti-setor-minimal", 
        "version": "1.0.0"
    })

@app.route('/test', methods=['GET'])
def test():
    print("🧪 Test endpoint called")
    return jsonify({
        "database": "not connected (test mode)",
        "ocr": "disabled (test mode - will add EasyOCR later)",
        "environment": {
            "PORT": os.environ.get('PORT', 'not set'),
            "FLASK_ENV": os.environ.get('FLASK_ENV', 'not set')
        }
    })

# API ENDPOINTS FOR BUKTI SETOR PROCESSING
@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_receipt():
    print("🧾 Process receipt endpoint called")
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        # For now, return a mock response since we don't have OCR yet
        return jsonify({
            "status": "success",
            "message": "Receipt processing endpoint working (OCR disabled in minimal mode)",
            "data": {
                "processed": True,
                "ocr_engine": "easyocr (disabled)",
                "filename": "test.jpg",
                "extracted_data": {
                    "bank_name": "Bank Test",
                    "account_number": "1234567890",
                    "transaction_amount": 500000,
                    "transaction_date": "2025-07-29",
                    "note": "This is a mock response - OCR will be added later"
                }
            },
            "timestamp": str(datetime.utcnow())
        }), 200
        
    except Exception as e:
        print(f"❌ Error in process_receipt: {e}")
        return jsonify({
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    print("📋 History endpoint called")
    return jsonify({
        "status": "success",
        "message": "History endpoint working (database disabled in minimal mode)",
        "data": {
            "receipts": [
                {
                    "id": 1,
                    "filename": "receipt1.jpg",
                    "processed_at": "2025-07-29T10:00:00Z",
                    "bank_name": "Bank Test 1",
                    "amount": 500000
                },
                {
                    "id": 2,
                    "filename": "receipt2.jpg", 
                    "processed_at": "2025-07-29T09:30:00Z",
                    "bank_name": "Bank Test 2",
                    "amount": 750000
                }
            ],
            "total": 2,
            "note": "This is mock data - database will be connected later"
        },
        "timestamp": str(datetime.utcnow())
    })

print("✅ All routes registered with CORS support")

print("✅ All routes registered")

if __name__ == '__main__':
    # Railway automatically sets PORT environment variable
    port = int(os.environ.get('PORT', 5002))
    print(f"🚀 Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
