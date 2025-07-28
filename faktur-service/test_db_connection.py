# ========================================
# DATABASE CONNECTION TEST - FAKTUR SERVICE
# ========================================

import os
import sys
from flask import Flask
from config import Config
from models import db, PPNMasukan, PPNKeluaran

def test_database_connection():
    """Test database connection for Faktur Service"""
    print("🚀 Testing Faktur Service Database Connection...")
    
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
            
            # Test tables
            print(f"📊 PPNMasukan table: {PPNMasukan.__tablename__}")
            print(f"📊 PPNKeluaran table: {PPNKeluaran.__tablename__}")
            
            # Test query
            masukan_count = PPNMasukan.query.count()
            keluaran_count = PPNKeluaran.query.count()
            
            print(f"📈 PPNMasukan records: {masukan_count}")
            print(f"📈 PPNKeluaran records: {keluaran_count}")
            
            print("✅ Faktur Service database test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

if __name__ == "__main__":
    test_database_connection()
