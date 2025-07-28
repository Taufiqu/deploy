# 🚀 Railway Deployment Guide - Separated Services

This guide will help you deploy the OCR application as two separate services on Railway:

## 📋 Overview

- **Faktur Service** (Port 5001) - Uses Tesseract OCR for invoice processing
- **Bukti Setor Service** (Port 5002) - Uses EasyOCR for payment receipt processing
- **Shared Database** - PostgreSQL (Supabase recommended)

## 🔧 Prerequisites

1. **Railway Account** - Sign up at [railway.app](https://railway.app)
2. **GitHub Repository** - Your code should be in a GitHub repository
3. **Database** - PostgreSQL database (Supabase recommended)

## 📦 Service 1: Faktur OCR Service (Tesseract)

### Step 1: Create New Railway Project
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway new
```

### Step 2: Configure Faktur Service
1. Connect your GitHub repository
2. Set the service name: `faktur-ocr-service`
3. Configure environment variables:

```env
DATABASE_URL=postgresql://postgres:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5001
POPPLER_PATH=/usr/bin
SECRET_KEY=your-secure-secret-key
SERVICE_NAME=faktur-ocr
```

### Step 3: Set Build Configuration
In Railway dashboard:
- **Build Command**: (empty - uses Dockerfile)
- **Dockerfile Path**: `Dockerfile.faktur`
- **Health Check Path**: `/health`

## 📦 Service 2: Bukti Setor OCR Service (EasyOCR)

### Step 1: Create Second Service
In the same Railway project:
1. Add new service
2. Connect same GitHub repository
3. Set service name: `bukti-setor-ocr-service`

### Step 2: Configure Bukti Setor Service
Set environment variables:

```env
DATABASE_URL=postgresql://postgres:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5002
POPPLER_PATH=/usr/bin
SECRET_KEY=your-secure-secret-key
SERVICE_NAME=bukti-setor-ocr
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
```

### Step 3: Set Build Configuration
- **Dockerfile Path**: `Dockerfile.bukti-setor`
- **Health Check Path**: `/health`

## 🗄️ Database Setup (Supabase)

### Option A: Use Supabase (Recommended)

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string from Settings > Database
4. Run migrations:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="your-supabase-connection-string"

# Run migrations
flask db upgrade
```

### Option B: Use Railway PostgreSQL

1. Add PostgreSQL service to your Railway project
2. Railway will auto-generate `DATABASE_URL`
3. Both services will share the same database

## 🚀 Deployment Steps

### 1. Prepare Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy Faktur Service
1. In Railway dashboard, go to Faktur service
2. Connect to GitHub repository
3. Set environment variables
4. Deploy

### 3. Deploy Bukti Setor Service
1. Create second service in same project
2. Connect to same GitHub repository
3. Set environment variables
4. Deploy

### 4. Verify Deployment
Check health endpoints:
- Faktur Service: `https://your-faktur-domain.railway.app/health`
- Bukti Setor Service: `https://your-bukti-setor-domain.railway.app/health`

## 🔧 Environment Variables Setup

### Required for Both Services:
```env
DATABASE_URL=postgresql://postgres:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=false
POPPLER_PATH=/usr/bin
SECRET_KEY=your-very-secure-secret-key
LOG_LEVEL=INFO
```

### Faktur Service Specific:
```env
PORT=5001
SERVICE_NAME=faktur-ocr
```

### Bukti Setor Service Specific:
```env
PORT=5002
SERVICE_NAME=bukti-setor-ocr
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
```

## 📡 API Endpoints

### Faktur Service Endpoints:
- `GET /health` - Health check
- `POST /api/faktur/upload` - Process invoice
- `GET /api/faktur/history/<jenis_pajak>` - Get history
- `GET /api/faktur/export/<jenis_pajak>` - Export to Excel
- `DELETE /api/faktur/delete/<id>` - Delete invoice

### Bukti Setor Service Endpoints:
- `GET /health` - Health check
- `GET /api/info` - Service information
- `POST /api/bukti-setor/upload` - Process receipt
- `GET /api/bukti-setor/history` - Get history
- `GET /api/laporan/export` - Export to Excel
- `DELETE /api/bukti-setor/delete/<id>` - Delete receipt

## 🔍 Monitoring & Troubleshooting

### Health Checks
Both services provide health check endpoints:
```bash
curl https://your-service.railway.app/health
```

### Logs
View logs in Railway dashboard or via CLI:
```bash
railway logs
```

### Common Issues

1. **Build Timeout**
   - Increase build timeout in Railway settings
   - EasyOCR service may need more time due to model downloads

2. **Memory Issues**
   - EasyOCR requires more memory
   - Consider upgrading Railway plan

3. **Database Connection**
   - Ensure DATABASE_URL is correctly formatted
   - Check SSL requirements for external databases

## 🔄 CI/CD Setup

Railway automatically deploys when you push to your connected GitHub branch:

```bash
git add .
git commit -m "Update application"
git push origin main
# Railway will automatically deploy both services
```

## 💰 Cost Optimization

### Resource Allocation:
- **Faktur Service**: Lower resource requirements (Tesseract is lighter)
- **Bukti Setor Service**: Higher resource requirements (EasyOCR + PyTorch)

### Scaling Strategy:
- Start with minimal resources
- Monitor usage and scale based on demand
- Consider using Railway's autoscaling features

## 🔒 Security Considerations

1. **Environment Variables**: Never commit sensitive data
2. **HTTPS**: Railway provides HTTPS by default
3. **CORS**: Configure CORS for production domains
4. **API Rate Limiting**: Consider implementing rate limiting
5. **File Upload Security**: Validate file types and sizes

## 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Supabase Documentation: [supabase.com/docs](https://supabase.com/docs)
- GitHub Issues: Create issues for application-specific problems
