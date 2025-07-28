# ========================================
# APLIKASI BUKTI SETOR - EASYOCR
# ========================================

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import Config
from models import db, BuktiSetor
from bukti_setor.routes import bukti_setor_bp, laporan_bp
from bukti_setor.services.delete import delete_bukti_setor

# ========================================
# FLASK APP INITIALIZATION
# ========================================
app = Flask(__name__)
app.config.from_object(Config)

# CORS Configuration for production
CORS(app, 
     origins=["*"],  # Configure specific domains in production
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False)

# Database initialization
db.init_app(app)

# Register blueprints
app.register_blueprint(bukti_setor_bp, url_prefix='/api')
app.register_blueprint(laporan_bp, url_prefix='/api')

# ========================================
# HEALTH CHECK ENDPOINT
# ========================================
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "service": "bukti-setor-ocr",
        "ocr_engine": "easyocr",
        "version": "1.0.0"
    }), 200

# ========================================
# SERVICE INFO ENDPOINT
# ========================================
@app.route('/api/info', methods=['GET'])
def service_info():
    """Get service information"""
    return jsonify({
        "service": "Bukti Setor OCR Service",
        "ocr_engine": "EasyOCR",
        "supported_languages": ["id", "en"],
        "supported_formats": ["PDF", "JPG", "PNG", "JPEG"],
        "features": [
            "OCR processing with EasyOCR",
            "Spell checking",
            "Data validation",
            "Excel export",
            "History tracking"
        ]
    }), 200

# ========================================
# DATABASE INITIALIZATION
# ========================================
def create_tables():
    """Create database tables if they don't exist"""
    try:
        db.create_all()
        print("✅ Database tables created for Bukti Setor service")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

# Initialize tables on startup (Flask 2.3+ compatible)
@app.before_request
def initialize_database():
    """Initialize database tables before first request"""
    if not hasattr(initialize_database, 'initialized'):
        with app.app_context():
            create_tables()
        initialize_database.initialized = True

# ========================================
# ERROR HANDLERS
# ========================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
