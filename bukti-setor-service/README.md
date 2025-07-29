# Bukti Setor Service - Railway Deployment

## Overview
This service provides OCR processing for Indonesian bank deposit receipts (bukti setor) using Tesseract OCR engine, optimized for Railway deployment.

## Key Features
- **Universal OCR Engine**: Supports both Tesseract and EasyOCR with automatic fallback
- **Railway Optimized**: Configured for Railway's environment and constraints
- **Health Check**: Built-in health endpoint for monitoring
- **PostgreSQL Support**: Compatible with Railway's PostgreSQL addon

## Railway Deployment

### Configuration Files
- `Dockerfile`: Main Docker configuration (Tesseract-based for lightweight deployment)
- `railway.json`: Railway-specific deployment configuration
- `requirements.txt`: Optimized Python dependencies for Railway
- `Procfile`: Alternative deployment method (if needed)

### Environment Variables
Required environment variables for Railway:
```
DATABASE_URL=postgresql://... (set by Railway PostgreSQL addon)
SECRET_KEY=your-secret-key
FLASK_ENV=production
PORT=5002 (set automatically by Railway)
```

### Health Check
The service provides a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "service": "bukti-setor-ocr",
  "ocr_engine": "tesseract",
  "version": "1.0.0"
}
```

### OCR Engine
- **Primary**: Tesseract OCR (lightweight, suitable for Railway)
- **Fallback**: EasyOCR (if available)
- **Languages**: Indonesian and English support

## API Endpoints
- `GET /health` - Health check
- `GET /api/info` - Service information
- `POST /api/process` - Process bukti setor documents (main OCR endpoint)

## Deployment Steps
1. Push code to GitHub
2. Connect repository to Railway
3. Railway will automatically detect Dockerfile
4. Add PostgreSQL addon
5. Set required environment variables
6. Deploy!

## File Structure
```
bukti-setor-service/
├── Dockerfile              # Main Docker config
├── railway.json           # Railway deployment config
├── requirements.txt       # Python dependencies
├── app_bukti_setor.py    # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
└── bukti_setor/          # Core OCR processing modules
    ├── routes/           # Flask routes
    ├── services/         # Business logic
    └── utils/            # OCR and processing utilities
```