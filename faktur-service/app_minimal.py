# ========================================
# FAKTUR SERVICE - WITH DATABASE & CORS & API ENDPOINTS
# ========================================

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, PPNMasukan

print("🚀 STARTING FAKTUR SERVICE WITH DATABASE & CORS...")
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

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database error: {e}")

print("✅ Flask app with CORS and Database created successfully")

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

# DATABASE CRUD ENDPOINTS
@app.route('/api/save-faktur', methods=['POST'])
def save_faktur():
    """Save processed faktur data to database"""
    try:
        data = request.get_json()
        print(f"📝 Saving faktur data: {data}")
        
        # Support bulk save
        if isinstance(data, list):
            saved_count = 0
            for item in data:
                if all(key in item for key in ['jenis', 'no_faktur', 'tanggal', 'nama_lawan_transaksi', 'dpp', 'ppn']):
                    tanggal_obj = datetime.strptime(item['tanggal'], '%Y-%m-%d').date()
                    
                    new_record = PPNMasukan(
                        jenis=item['jenis'],
                        no_faktur=item['no_faktur'],
                        tanggal=tanggal_obj,
                        nama_lawan_transaksi=item['nama_lawan_transaksi'],
                        dpp=float(item['dpp']),
                        ppn=float(item['ppn'])
                    )
                    db.session.add(new_record)
                    saved_count += 1
            
            db.session.commit()
            return jsonify(message=f"{saved_count} faktur berhasil disimpan!"), 201
        
        # Single record save
        else:
            if not all(key in data for key in ['jenis', 'no_faktur', 'tanggal', 'nama_lawan_transaksi', 'dpp', 'ppn']):
                return jsonify(error="Field tidak lengkap"), 400
            
            tanggal_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
            
            new_record = PPNMasukan(
                jenis=data['jenis'],
                no_faktur=data['no_faktur'],
                tanggal=tanggal_obj,
                nama_lawan_transaksi=data['nama_lawan_transaksi'],
                dpp=float(data['dpp']),
                ppn=float(data['ppn'])
            )
            
            db.session.add(new_record)
            db.session.commit()
            return jsonify(message="Faktur berhasil disimpan!"), 201
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saving faktur: {e}")
        return jsonify(error=f"Error saving faktur: {str(e)}"), 500

@app.route('/api/faktur-history', methods=['GET'])
def get_faktur_history():
    """Get all faktur records"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        print(f"📋 Fetching faktur history - Page: {page}, Per page: {per_page}")
        
        results = db.session.execute(
            db.select(PPNMasukan)
            .order_by(PPNMasukan.tanggal.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).scalars().all()
        
        data = [record.to_dict() for record in results]
        return jsonify(message="Data berhasil diambil.", data=data, total=len(data)), 200
        
    except Exception as e:
        print(f"❌ Error fetching faktur history: {e}")
        return jsonify(error=f"Error fetching data: {str(e)}"), 500

@app.route('/api/faktur/<int:id>', methods=['DELETE'])
def delete_faktur(id):
    """Delete faktur record by ID"""
    try:
        print(f"🗑️ Deleting faktur ID: {id}")
        
        record = db.session.get(PPNMasukan, id)
        if not record:
            return jsonify(error="Data tidak ditemukan"), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify(message="Data berhasil dihapus"), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting faktur: {e}")
        return jsonify(error=f"Error deleting data: {str(e)}"), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Legacy endpoint - redirect to faktur-history"""
    return get_faktur_history()

print("✅ All routes registered with CORS support")

if __name__ == '__main__':
    # Railway automatically sets PORT environment variable
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
