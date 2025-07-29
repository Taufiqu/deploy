# ========================================
# FAKTUR SERVICE - PRODUCTION READY
# ========================================

import os
import sys
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables (optional file)
try:
    load_dotenv('.env.local')
except:
    # File not found, which is OK for production
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("🚀 STARTING FAKTUR SERVICE - PRODUCTION...")
logger.info(f"📊 Python version: {sys.version}")

# Database Models Import with Error Handling
DATABASE_AVAILABLE = False
try:
    from models import db, PpnMasukan, PpnKeluaran
    logger.info("✅ Database models imported successfully")
    DATABASE_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Database models import failed: {e}")
    logger.error("❌ Running without database functionality")

# Create Flask app
app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=["*", "https://pajak-ocr.vercel.app", "http://localhost:3000"],  # Allow Vercel domain
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False)

# Basic Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Database Configuration
if DATABASE_AVAILABLE:
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Debug: log raw connection string format (hide password)
        masked_url = database_url[:50] + "***" + database_url[-20:] if len(database_url) > 70 else database_url
        logger.info(f"� Raw DATABASE_URL: {masked_url}")
        
        # Debug: check if URL format is correct
        if not database_url.startswith('postgresql://'):
            logger.error(f"❌ Invalid DATABASE_URL format! Must start with 'postgresql://', got: {database_url[:20]}...")
            DATABASE_AVAILABLE = False
        else:
            # Use standard postgresql:// for psycopg2
            logger.info(f"🔄 Using psycopg2 driver")
            
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                'pool_pre_ping': True,
                'pool_recycle': 300,
                'pool_timeout': 30,
            }
        
        # Initialize database
        try:
            db.init_app(app)
            
            # Test database connection
            with app.app_context():
                db.create_all()
                # Test query
                result = db.session.execute(db.text("SELECT 1")).fetchone()
                logger.info("✅ Database connection successful")
                
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            DATABASE_AVAILABLE = False
    else:
        logger.error("❌ DATABASE_URL not set")
        DATABASE_AVAILABLE = False

logger.info("✅ Flask app with CORS created successfully")

# ========================================
# ROUTE HANDLERS
# ========================================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "service": "faktur-service",
        "status": "running",
        "database_available": DATABASE_AVAILABLE,
        "timestamp": str(datetime.utcnow()),
        "version": "1.0.0"
    })

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "service": "faktur-service", 
        "database_available": DATABASE_AVAILABLE,
        "database_url_set": bool(os.getenv('DATABASE_URL')),
        "environment": os.getenv('ENVIRONMENT', 'production')
    })

@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Test database connection and operations"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Test query on ppn_masukan table
        result_masukan = db.session.execute(
            db.text("SELECT COUNT(*) FROM ppn_masukan")
        ).fetchone()
        count_masukan = result_masukan[0] if result_masukan else 0
        
        # Test query on ppn_keluaran table  
        result_keluaran = db.session.execute(
            db.text("SELECT COUNT(*) FROM ppn_keluaran")
        ).fetchone()
        count_keluaran = result_keluaran[0] if result_keluaran else 0
        
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "tables": {
                "ppn_masukan": count_masukan,
                "ppn_keluaran": count_keluaran
            },
            "database_url": os.getenv('DATABASE_URL')[:50] + "..." if os.getenv('DATABASE_URL') else None
        })
        
    except Exception as e:
        logger.error(f"Database test error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/api/save-faktur', methods=['POST'])
def save_faktur():
    """Save faktur data to database"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        data = request.get_json()
        logger.info(f"📝 Saving faktur: {data}")
        
        # Validate required fields
        required_fields = ['bulan', 'no_faktur', 'tanggal', 'npwp_lawan_transaksi', 'nama_lawan_transaksi', 'dpp', 'ppn']
        if not data or not all(key in data for key in required_fields):
            return jsonify({
                "status": "error",
                "message": "Required fields: bulan, no_faktur, tanggal, npwp_lawan_transaksi, nama_lawan_transaksi, dpp, ppn"
            }), 400
        
        # Parse date
        tanggal_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
        
        # Determine which table to use based on jenis
        jenis = data.get('jenis', 'masukan').lower()
        if jenis == 'masukan':
            new_record = PpnMasukan(
                bulan=data['bulan'],
                no_faktur=data['no_faktur'],
                tanggal=tanggal_obj,
                keterangan=data.get('keterangan'),
                npwp_lawan_transaksi=data['npwp_lawan_transaksi'],
                nama_lawan_transaksi=data['nama_lawan_transaksi'],
                dpp=float(data['dpp']),
                ppn=float(data['ppn'])
            )
        elif jenis == 'keluaran':
            new_record = PpnKeluaran(
                bulan=data['bulan'],
                no_faktur=data['no_faktur'],
                tanggal=tanggal_obj,
                keterangan=data.get('keterangan'),
                npwp_lawan_transaksi=data['npwp_lawan_transaksi'],
                nama_lawan_transaksi=data['nama_lawan_transaksi'],
                dpp=float(data['dpp']),
                ppn=float(data['ppn'])
            )
        else:
            return jsonify({
                "status": "error",
                "message": "Jenis must be 'masukan' or 'keluaran'"
            }), 400
        
        db.session.add(new_record)
        db.session.commit()
        
        logger.info(f"✅ Record saved successfully: {new_record.no_faktur}")
        
        return jsonify({
            "status": "success",
            "message": "Faktur saved successfully!",
            "data": new_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Save faktur error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/faktur-history', methods=['GET'])
def get_faktur_history():
    """Get faktur records"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Get query parameters
        jenis = request.args.get('jenis', 'all')  # 'masukan', 'keluaran', or 'all'
        limit = min(int(request.args.get('limit', 20)), 100)  # Max 100 records
        
        results = []
        
        if jenis == 'all' or jenis == 'masukan':
            masukan_results = db.session.execute(
                db.select(PpnMasukan)
                .order_by(PpnMasukan.created_at.desc())
                .limit(limit)
            ).scalars().all()
            results.extend([record.to_dict() for record in masukan_results])
        
        if jenis == 'all' or jenis == 'keluaran':
            keluaran_results = db.session.execute(
                db.select(PpnKeluaran)
                .order_by(PpnKeluaran.created_at.desc())
                .limit(limit)
            ).scalars().all()
            results.extend([record.to_dict() for record in keluaran_results])
        
        # Sort by created_at if getting all
        if jenis == 'all':
            results.sort(key=lambda x: x['created_at'], reverse=True)
            results = results[:limit]  # Apply limit after sorting
        
        return jsonify({
            "status": "success",
            "message": "Data retrieved successfully",
            "data": results,
            "total": len(results),
            "jenis": jenis
        })
        
    except Exception as e:
        logger.error(f"Get history error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/faktur/<int:faktur_id>', methods=['DELETE'])
def delete_faktur(faktur_id):
    """Delete a faktur record"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Try to find in both tables
        record = None
        table_name = None
        
        # Check ppn_masukan first
        record = db.session.get(PpnMasukan, faktur_id)
        if record:
            table_name = "ppn_masukan"
        else:
            # Check ppn_keluaran
            record = db.session.get(PpnKeluaran, faktur_id)
            if record:
                table_name = "ppn_keluaran"
        
        if not record:
            return jsonify({
                "status": "error",
                "message": "Record not found"
            }), 404
        
        # Delete the record
        db.session.delete(record)
        db.session.commit()
        
        logger.info(f"✅ Record deleted successfully from {table_name}: {faktur_id}")
        
        return jsonify({
            "status": "success",
            "message": f"Record deleted successfully from {table_name}",
            "deleted_id": faktur_id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete faktur error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_upload():
    """Process uploaded file - main endpoint for frontend"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({"status": "ok"}), 200
    
    try:
        logger.info(f"📤 Processing upload request from: {request.origin}")
        
        # Check if database is available
        if not DATABASE_AVAILABLE:
            return jsonify({
                "status": "error",
                "message": "Database service temporarily unavailable",
                "code": "DB_UNAVAILABLE"
            }), 503
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded",
                "code": "NO_FILE"
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No file selected",
                "code": "EMPTY_FILE"
            }), 400
        
        # For now, return success with placeholder data
        # TODO: Implement actual OCR processing with Tesseract
        
        placeholder_data = {
            "jenis": "masukan",
            "no_faktur": f"DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "tanggal": datetime.now().strftime('%Y-%m-%d'),
            "nama_lawan_transaksi": "Demo Company",
            "dpp": 1000000,
            "ppn": 100000,
            "filename": file.filename
        }
        
        logger.info(f"📝 Demo processing completed for: {file.filename}")
        
        return jsonify({
            "status": "success",
            "message": "File processed successfully (DEMO MODE)",
            "data": placeholder_data,
            "note": "This is demo mode. OCR processing will be implemented next."
        }), 200
        
    except Exception as e:
        logger.error(f"Process upload error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Processing failed: {str(e)}",
            "code": "PROCESS_ERROR"
        }), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error", 
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Starting production server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
