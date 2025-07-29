# ========================================
# FAKTUR SERVICE - LOCAL TESTING WITH DATABASE
# ========================================

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

print("🚀 STARTING FAKTUR SERVICE - LOCAL TESTING...")
print(f"📊 Python version: {sys.version}")
print(f"📊 DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')[:50]}...")

# Try to import database models
try:
    from models import db, PPNMasukan
    print("✅ Database models imported successfully")
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"❌ Database models import failed: {e}")
    DATABASE_AVAILABLE = False

# Create Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False)

# Basic config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-secret-key')

# Database configuration
if DATABASE_AVAILABLE:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Initialize database
    db.init_app(app)
    
    # Test database connection
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database connection successful and tables created")
            
            # Test query
            result = db.session.execute(db.text("SELECT 1")).fetchone()
            print(f"✅ Database query test successful: {result}")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            DATABASE_AVAILABLE = False

print("✅ Flask app with CORS created successfully")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "faktur-local-testing",
        "status": "running",
        "database_available": DATABASE_AVAILABLE,
        "timestamp": str(datetime.utcnow())
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "faktur-local-testing", 
        "database_available": DATABASE_AVAILABLE,
        "database_url_set": bool(os.getenv('DATABASE_URL'))
    })

@app.route('/test-db', methods=['GET'])
def test_database():
    """Test database connection and operations"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Test basic query
        result = db.session.execute(db.text("SELECT COUNT(*) FROM ppn_masukan")).fetchone()
        count = result[0] if result else 0
        
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "total_records": count,
            "database_url": os.getenv('DATABASE_URL')[:50] + "..."
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/api/save-faktur', methods=['POST'])
def save_faktur():
    """Test save faktur data"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        data = request.get_json()
        print(f"📝 Testing save faktur: {data}")
        
        # Create test record if no data provided
        if not data:
            data = {
                "jenis": "masukan",
                "no_faktur": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "tanggal": "2025-01-15",
                "nama_lawan_transaksi": "Test Company",
                "dpp": 100000,
                "ppn": 10000
            }
        
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
        
        return jsonify({
            "status": "success",
            "message": "Test record saved successfully!",
            "data": new_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/faktur-history', methods=['GET'])
def get_faktur_history():
    """Test get faktur records"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        results = db.session.execute(
            db.select(PPNMasukan)
            .order_by(PPNMasukan.created_at.desc())
            .limit(10)
        ).scalars().all()
        
        data = [record.to_dict() for record in results]
        
        return jsonify({
            "status": "success",
            "message": "Data retrieved successfully",
            "data": data,
            "total": len(data)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting local testing server on port {port}")
    print("🔗 Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=port, debug=True)
