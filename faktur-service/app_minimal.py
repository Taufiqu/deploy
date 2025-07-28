# ========================================
# MINIMAL FLASK APP - FOR TESTING DEPLOYMENT ONLY
# ========================================

import os
from datetime import datetime
from flask import Flask, jsonify

# Create Flask app
app = Flask(__name__)

# Basic config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-secret-key')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "faktur-minimal",
        "status": "running",
        "message": "Deployment test successful!",
        "timestamp": str(datetime.utcnow())
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "faktur-minimal", 
        "version": "1.0.0"
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "database": "not connected (test mode)",
        "ocr": "disabled (test mode)",
        "environment": {
            "PORT": os.environ.get('PORT', 'not set'),
            "FLASK_ENV": os.environ.get('FLASK_ENV', 'not set')
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
