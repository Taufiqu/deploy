# ========================================
# DATABASE CONNECTION TEST - BUKTI SETOR SERVICE
# ========================================

import os
import sys
from flask import Flask
from config import Config
from models import db, BuktiSetor

def test_database_connection():
    """Test database connection for Bukti Setor Service"""
    print("🚀 Testing Bukti Setor Service Database Connection...")
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Test connection
            db.create_all()
            print("✅ Database connection successful!")
            
            # Test table
            print(f"📊 BuktiSetor table: {BuktiSetor.__tablename__}")
            
            # Test query
            bukti_setor_count = BuktiSetor.query.count()
            
            print(f"📈 BuktiSetor records: {bukti_setor_count}")
            
            print("✅ Bukti Setor Service database test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

if __name__ == "__main__":
    test_database_connection()
