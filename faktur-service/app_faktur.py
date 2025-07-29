# ========================================
# APLIKASI FAKTUR - TESSERACT OCR
# ========================================

import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import Config
from models import db, PPNMasukan, PPNKeluaran
from faktur.services import (
    process_invoice_file,
    save_invoice_data,
    generate_excel_export,
    get_history,
)
from faktur.services.delete import delete_faktur

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

# ========================================
# HEALTH CHECK ENDPOINT
# ========================================
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint for Railway - no DB dependency"""
    try:
        return {
            "status": "healthy",
            "service": "faktur-ocr",
            "ocr_engine": "tesseract",
            "version": "1.0.0",
            "timestamp": str(datetime.utcnow())
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy", 
            "error": str(e)
        }, 500

@app.route('/health/full', methods=['GET'])
def health_check_full():
    """Full health check with database"""
    try:
        # Test database connection
        result = db.session.execute(db.text("SELECT 1"))
        test_value = result.fetchone()[0]
        
        return jsonify({
            "status": "healthy",
            "service": "faktur-ocr",
            "ocr_engine": "tesseract", 
            "version": "1.0.0",
            "database": "connected" if test_value == 1 else "error",
            "timestamp": str(datetime.utcnow())
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "faktur-ocr",
            "error": str(e)
        }), 500

# ========================================
# FAKTUR PROCESSING ENDPOINTS
# ========================================
@app.route('/api/faktur/upload', methods=['POST'])
def upload_faktur():
    """Upload and process faktur using Tesseract OCR"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get jenis_pajak from request
        jenis_pajak = request.form.get('jenis_pajak', 'masukan')
        
        # Process file using Tesseract OCR
        result = process_invoice_file(request, app.config)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Save to database
        save_result = save_invoice_data(result, jenis_pajak)
        
        return jsonify({
            "message": "Faktur processed successfully",
            "data": result,
            "saved": save_result,
            "ocr_engine": "tesseract"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route('/api/faktur/history/<jenis_pajak>', methods=['GET'])
def faktur_history(jenis_pajak):
    """Get faktur history"""
    try:
        history_data = get_history(jenis_pajak)
        return jsonify({
            "data": history_data,
            "count": len(history_data)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/faktur/export/<jenis_pajak>', methods=['GET'])
def export_faktur(jenis_pajak):
    """Export faktur to Excel"""
    try:
        file_path = generate_excel_export(jenis_pajak)
        return jsonify({
            "message": "Excel generated successfully",
            "file_path": file_path
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/faktur/delete/<int:faktur_id>', methods=['DELETE'])
def delete_faktur_endpoint(faktur_id):
    """Delete faktur by ID"""
    try:
        jenis_pajak = request.args.get('jenis_pajak', 'masukan')
        result = delete_faktur(faktur_id, jenis_pajak)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================
# DATABASE INITIALIZATION
# ========================================
def create_tables():
    """Create database tables if they don't exist"""
    try:
        db.create_all()
        print("✅ Database tables created for Faktur service")
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
