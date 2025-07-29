# ========================================
# MINIMAL FLASK APP - FOR TESTING DEPLOYMENT ONLY
# ========================================

import os
import sys
from datetime import datetime
from flask import Flask, jsonify

print("🚀 STARTING MINIMAL FLASK APP...")
print(f"📊 Python version: {sys.version}")
print(f"📊 PORT environment: {os.environ.get('PORT', 'NOT SET')}")

# Create Flask app
app = Flask(__name__)

# Basic config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-secret-key')

print("✅ Flask app created successfully")

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

print("✅ All routes registered")

if __name__ == '__main__':
    # Railway automatically sets PORT environment variable
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
