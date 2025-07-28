# File: backend/config.py

import os
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

class Config:
    """Konfigurasi utama aplikasi Flask."""

    # ========================================
    # DATABASE CONFIGURATION
    # ========================================
    
    # Mengambil URI database dari environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Handle Railway's PostgreSQL URL format
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///default.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database connection configuration for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 30,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'sslmode': 'require',
            'connect_timeout': 10
        } if DATABASE_URL else {}
    }

    # ========================================
    # APPLICATION CONFIGURATION
    # ========================================
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Environment settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = "uploads"
    
    # ========================================
    # OCR CONFIGURATION
    # ========================================
    
    # Poppler path for PDF processing
    POPPLER_PATH = os.getenv("POPPLER_PATH", "/usr/bin")
    
    # OCR settings
    OCR_TIMEOUT = int(os.getenv('OCR_TIMEOUT', '30'))
    OCR_MAX_RETRIES = int(os.getenv('OCR_MAX_RETRIES', '3'))
    
    # ========================================
    # RAILWAY SPECIFIC CONFIGURATION
    # ========================================
    
    # Railway deployment settings
    PORT = int(os.getenv('PORT', 5000))
    RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', '')
    RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
    
    # ========================================
    # LOGGING CONFIGURATION
    # ========================================
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # ========================================
    # DEVELOPMENT HELPER
    # ========================================
    
    @classmethod
    def init_app(cls, app):
        """Initialize application configuration"""
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER)
            print(f"✅ Created upload folder: {cls.UPLOAD_FOLDER}")
        
        # Debug information (only in development)
        if cls.DEBUG:
            print("🔍 Database URL:", DATABASE_URL[:50] + "..." if DATABASE_URL and len(DATABASE_URL) > 50 else DATABASE_URL)
            print("📦 POPPLER PATH:", cls.POPPLER_PATH)
            print("🔧 Environment:", cls.FLASK_ENV)
            print("🚪 Port:", cls.PORT)
