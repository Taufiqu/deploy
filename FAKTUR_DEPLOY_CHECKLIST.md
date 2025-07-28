# 🎯 FAKTUR SERVICE DEPLOYMENT CHECKLIST
# =====================================================

## ✅ READY TO DEPLOY - FAKTUR SERVICE ONLY

### 📋 Pre-Deploy Verification:

**✅ Files Ready:**
- ✅ `Dockerfile` - Minimal, clean, production-ready
- ✅ `requirements.txt` - Only essential dependencies (~15 packages)
- ✅ `Procfile` - Gunicorn configuration  
- ✅ `nixpacks.toml` - Force Dockerfile build
- ✅ `railway.json` - Railway configuration
- ✅ `/health` endpoint - Available in app_faktur.py

**✅ Dependencies Verified:**
- ✅ **Flask 2.3.3** - Core framework
- ✅ **psycopg2-binary** - Database connection
- ✅ **pytesseract** - OCR engine
- ✅ **Pillow** - Image processing
- ✅ **gunicorn** - Production server

**✅ Build Strategy:**
- ✅ **Python 3.11-slim** base image
- ✅ **Tesseract OCR** system dependency
- ✅ **Minimal system packages** only
- ✅ **Single worker** configuration
- ✅ **Health check** configured

### 🚀 RAILWAY DEPLOYMENT STEPS:

#### Step 1: Create New Project
1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `Taufiqu/deploy`

#### Step 2: Configure Root Directory
⚠️ **CRITICAL**: Set **Root Directory = `faktur-service`**

#### Step 3: Environment Variables
Add these in Railway dashboard:
```
DATABASE_URL=postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://hodllrhwyqhrksfkgiqc.supabase.co
FLASK_ENV=production
SECRET_KEY=railway-production-secret-key-2025
```

#### Step 4: Deploy & Monitor
- ✅ Expected build time: **5-8 minutes**
- ✅ Build should succeed (minimal dependencies)
- ✅ Service will be available at Railway URL

### 🎯 Expected Result:
```
✅ Build Success
✅ Deploy Success  
✅ Health Check: https://faktur-xxx.up.railway.app/health
✅ API Ready: https://faktur-xxx.up.railway.app/process-invoice
```

### 🔍 If Build Fails:
1. Check Railway logs for specific error
2. Verify Root Directory = `faktur-service`
3. Check environment variables
4. Try redeploy

### 📊 Post-Deploy Testing:
```bash
# Test health endpoint
curl https://your-faktur-url.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "service": "faktur-ocr", 
  "ocr_engine": "tesseract",
  "version": "1.0.0"
}
```

---
## 🎉 DEPLOY FAKTUR SERVICE NOW!

**Command:** Go to Railway → New Project → Root: `faktur-service` → Deploy

**After faktur success, we can tackle bukti-setor service!**
