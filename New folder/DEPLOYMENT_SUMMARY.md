# 📋 Railway Deployment Summary

## ✅ What We've Accomplished

### 🔄 Service Separation
- **Faktur Service** (`app_faktur.py`) - Dedicated to Tesseract OCR
- **Bukti Setor Service** (`app_bukti_setor.py`) - Dedicated to EasyOCR
- **Shared Database** - PostgreSQL for both services

### 📁 Files Created/Modified

#### Application Files
- `app_faktur.py` - Faktur service main application
- `app_bukti_setor.py` - Bukti setor service main application
- `config.py` - Updated for production deployment

#### Docker Configuration
- `Dockerfile.faktur` - Container for Tesseract OCR service
- `Dockerfile.bukti-setor` - Container for EasyOCR service
- `docker-compose.dev.yml` - Local development environment

#### Railway Configuration
- `railway-faktur.toml` - Railway config for faktur service
- `railway-bukti-setor.toml` - Railway config for bukti setor service
- `Procfile.faktur` - Process file for faktur service
- `Procfile.bukti-setor` - Process file for bukti setor service

#### Dependencies
- `requirements-faktur.txt` - Dependencies for Tesseract service
- `requirements-bukti-setor.txt` - Dependencies for EasyOCR service

#### Documentation
- `RAILWAY_DEPLOYMENT.md` - Complete deployment guide
- `API_DOCS_SEPARATED.md` - API documentation for separated services
- `.env.example` - Updated environment variables template

#### Development Tools
- `dev-setup.sh` - Linux/Mac development setup script
- `dev-setup.bat` - Windows development setup script

---

## 🚀 Next Steps for Railway Deployment

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Configure separate services for Railway deployment"
git push origin main
```

### Step 2: Create Railway Projects

#### Option A: Two Separate Projects (Recommended)
1. **Project 1: Faktur OCR Service**
   - Repository: Your GitHub repo
   - Dockerfile: `Dockerfile.faktur`
   - Environment variables from `.env.example`

2. **Project 2: Bukti Setor OCR Service**
   - Repository: Your GitHub repo
   - Dockerfile: `Dockerfile.bukti-setor`
   - Environment variables from `.env.example`

#### Option B: Single Project with Multiple Services
1. Create one Railway project
2. Add two services within the same project
3. Both services share the same database

### Step 3: Database Setup

#### Option A: Supabase (Recommended)
```env
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres
```

#### Option B: Railway PostgreSQL
```bash
# Railway will auto-generate this
DATABASE_URL=postgresql://postgres:password@host.railway.internal:5432/railway
```

### Step 4: Environment Variables

#### For Faktur Service:
```env
DATABASE_URL=your-database-url
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5001
POPPLER_PATH=/usr/bin
SECRET_KEY=your-secure-secret-key
SERVICE_NAME=faktur-ocr
```

#### For Bukti Setor Service:
```env
DATABASE_URL=your-database-url
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5002
POPPLER_PATH=/usr/bin
SECRET_KEY=your-secure-secret-key
SERVICE_NAME=bukti-setor-ocr
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
```

---

## 🔧 Local Development

### Quick Start
```bash
# Windows
dev-setup.bat

# Linux/Mac
chmod +x dev-setup.sh
./dev-setup.sh
```

### Manual Setup
```bash
# Copy environment file
cp .env.example .env

# Update .env with your settings
# Then start services
docker-compose -f docker-compose.dev.yml up --build
```

### Service URLs (Development)
- **Faktur Service**: http://localhost:5001
- **Bukti Setor Service**: http://localhost:5002
- **Database**: localhost:5432

---

## 🎯 Service Characteristics

### Faktur Service (Tesseract)
- **Lighter Resource Usage** - Tesseract is CPU-based
- **Faster Startup** - No model downloads required
- **Better for Text-Heavy Documents** - Invoice processing
- **Port**: 5001

### Bukti Setor Service (EasyOCR)
- **Higher Resource Usage** - PyTorch + EasyOCR models
- **Slower Startup** - Pre-downloads ML models
- **Better for Image-Heavy Documents** - Receipt processing
- **Port**: 5002

---

## 📊 Estimated Resource Requirements

### Faktur Service
- **CPU**: 0.5 vCPU
- **Memory**: 512MB - 1GB
- **Storage**: 1GB

### Bukti Setor Service
- **CPU**: 1 vCPU
- **Memory**: 1GB - 2GB
- **Storage**: 2GB (includes EasyOCR models)

### Database
- **Storage**: Based on usage
- **Connections**: Both services will connect

---

## 🔍 Monitoring & Health Checks

### Health Check Endpoints
- Faktur: `/health`
- Bukti Setor: `/health`

### Response Example
```json
{
  "status": "healthy",
  "service": "faktur-ocr",
  "ocr_engine": "tesseract",
  "version": "1.0.0"
}
```

---

## 🚨 Troubleshooting

### Common Issues

1. **Build Timeout on EasyOCR Service**
   - Increase Railway build timeout
   - Models are pre-downloaded in Dockerfile

2. **Memory Issues**
   - EasyOCR service needs more memory
   - Consider Railway Pro plan

3. **Database Connection**
   - Ensure `DATABASE_URL` is correctly formatted
   - Check SSL requirements

4. **Port Conflicts**
   - Services use different ports (5001, 5002)
   - Railway auto-assigns external URLs

### Debug Commands
```bash
# Check service logs
railway logs

# Test health endpoints
curl https://your-service.railway.app/health

# Check database connection
railway run python -c "from models import db; print('DB connected')"
```

---

## 📝 File Structure Summary

```
your-project/
├── app_faktur.py              # Faktur service main app
├── app_bukti_setor.py         # Bukti setor service main app
├── config.py                  # Updated configuration
├── Dockerfile.faktur          # Faktur service container
├── Dockerfile.bukti-setor     # Bukti setor service container
├── docker-compose.dev.yml     # Development environment
├── requirements-faktur.txt    # Faktur dependencies
├── requirements-bukti-setor.txt # Bukti setor dependencies
├── railway-faktur.toml        # Railway config for faktur
├── railway-bukti-setor.toml   # Railway config for bukti setor
├── Procfile.faktur           # Process file for faktur
├── Procfile.bukti-setor      # Process file for bukti setor
├── RAILWAY_DEPLOYMENT.md     # Deployment guide
├── API_DOCS_SEPARATED.md     # API documentation
├── dev-setup.sh              # Linux/Mac setup script
├── dev-setup.bat             # Windows setup script
└── .env.example              # Environment template
```

---

## 🎉 Ready for Deployment!

Your application is now configured for Railway deployment with separated services. Each OCR engine runs independently, providing better resource management and scalability.

Follow the `RAILWAY_DEPLOYMENT.md` guide for detailed deployment instructions.
