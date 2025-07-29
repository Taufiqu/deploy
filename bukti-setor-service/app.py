# ========================================
# BUKTI SETOR SERVICE - PRODUCTION READY
# ========================================

import os
import sys
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("🚀 STARTING BUKTI SETOR SERVICE - PRODUCTION...")
logger.info(f"📊 Python version: {sys.version}")

# Database Models Import with Error Handling
DATABASE_AVAILABLE = False
try:
    from models import db, BuktiSetor
    logger.info("✅ Database models imported successfully")
    DATABASE_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Database models import failed: {e}")
    logger.error("❌ Running without database functionality")

# Create Flask app
app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=["*"],  # For Railway, allow all origins
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False)

# Basic Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Database Configuration
if DATABASE_AVAILABLE:
    database_url = os.getenv('DATABASE_URL')
    if database_url:
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
        "service": "bukti-setor-service",
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
        "service": "bukti-setor-service", 
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
        # Test query on bukti_setor table
        result = db.session.execute(
            db.text("SELECT COUNT(*) FROM bukti_setor")
        ).fetchone()
        count = result[0] if result else 0
        
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "total_bukti_setor": count,
            "database_url": os.getenv('DATABASE_URL')[:50] + "..." if os.getenv('DATABASE_URL') else None
        })
        
    except Exception as e:
        logger.error(f"Database test error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/api/save-bukti-setor', methods=['POST'])
def save_bukti_setor():
    """Save bukti setor data to database"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        data = request.get_json()
        logger.info(f"📝 Saving bukti setor: {data}")
        
        # Validate required fields
        required_fields = [
            'tanggal', 'kode_setor', 'jumlah'
        ]
        if not data or not all(key in data for key in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Required fields: {', '.join(required_fields)}"
            }), 400
        
        # Parse date
        tanggal_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
        
        new_record = BuktiSetor(
            tanggal=tanggal_obj,
            kode_setor=data['kode_setor'],
            jumlah=float(data['jumlah'])
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        logger.info(f"✅ Record saved successfully: {new_record.kode_setor}")
        
        return jsonify({
            "status": "success",
            "message": "Bukti setor saved successfully!",
            "data": new_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Save bukti setor error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/bukti-setor-history', methods=['GET'])
def get_bukti_setor_history():
    """Get bukti setor records"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Get query parameters
        tahun = request.args.get('tahun')
        limit = min(int(request.args.get('limit', 20)), 100)  # Max 100 records
        
        # Build query
        query = db.select(BuktiSetor).order_by(BuktiSetor.created_at.desc())
        
        # Apply filters
        if tahun:
            # Filter by year from tanggal field
            query = query.where(db.extract('year', BuktiSetor.tanggal) == int(tahun))
        
        # Apply limit
        query = query.limit(limit)
        
        results = db.session.execute(query).scalars().all()
        data = [record.to_dict() for record in results]
        
        return jsonify({
            "status": "success",
            "message": "Data retrieved successfully",
            "data": data,
            "total": len(data),
            "filters": {
                "tahun": tahun
            }
        })
        
    except Exception as e:
        logger.error(f"Get history error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/bukti-setor/<int:bukti_setor_id>', methods=['DELETE'])
def delete_bukti_setor(bukti_setor_id):
    """Delete a bukti setor record"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Find the record
        record = db.session.get(BuktiSetor, bukti_setor_id)
        
        if not record:
            return jsonify({
                "status": "error",
                "message": "Record not found"
            }), 404
        
        # Delete the record
        db.session.delete(record)
        db.session.commit()
        
        logger.info(f"✅ Record deleted successfully: {bukti_setor_id}")
        
        return jsonify({
            "status": "success",
            "message": "Record deleted successfully",
            "deleted_id": bukti_setor_id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete bukti setor error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get summary statistics"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database not available"
        }), 500
    
    try:
        # Get current year
        current_year = datetime.now().year
        tahun_filter = request.args.get('tahun', current_year)
        
        # Get summary statistics
        total_count = db.session.execute(
            db.text("SELECT COUNT(*) FROM bukti_setor WHERE EXTRACT(YEAR FROM tanggal) = :tahun"),
            {"tahun": tahun_filter}
        ).fetchone()[0]
        
        total_amount = db.session.execute(
            db.text("SELECT COALESCE(SUM(jumlah), 0) FROM bukti_setor WHERE EXTRACT(YEAR FROM tanggal) = :tahun"),
            {"tahun": tahun_filter}
        ).fetchone()[0]
        
        return jsonify({
            "status": "success",
            "message": "Summary retrieved successfully",
            "summary": {
                "tahun": int(tahun_filter),
                "total_bukti_setor": total_count,
                "total_amount": float(total_amount) if total_amount else 0
            }
        })
        
    except Exception as e:
        logger.error(f"Get summary error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
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
    port = int(os.environ.get('PORT', 5001))
    logger.info(f"🚀 Starting production server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
