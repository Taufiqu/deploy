# 🚂 RAILWAY DEPLOYMENT - STEP BY STEP GUIDE

## ✅ DATABASE SETUP STATUS
- ✅ Supabase project: hodllrhwyqhrksfkgiqc
- ✅ Tables created: ppn_masukan, ppn_keluaran, bukti_setor
- ✅ Database credentials: Ready
- ✅ Environment configurations: Complete

---

## 🚀 PART 1: DEPLOY FAKTUR SERVICE

### Step 1.1: Create Railway Project
1. Go to [Railway](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. **IMPORTANT**: Set these configurations:

#### Build Configuration:
```
Root Directory: faktur-service
Dockerfile Path: Dockerfile.faktur
Port: 5001
```

#### Environment Variables (Copy from railway_env_faktur.txt):
```env
DATABASE_URL=postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://hodllrhwyqhrksfkgiqc.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvZGxscmh3eXFocmtzZmtnaXFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjY3NjQyMCwiZXhwIjoyMDUyMjUyNDIwfQ.lAOT5VnU8Kev-aOSDnpG6_Sojsg_SU8-TS1y0YE57Zw
FLASK_ENV=production
FLASK_APP=app_faktur.py
FLASK_DEBUG=false
SECRET_KEY=faktur-production-secret-key-very-secure-32-chars-minimum
PORT=5001
SERVICE_NAME=faktur-ocr-service
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=30
OCR_MAX_RETRIES=3
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=INFO
```

### Step 1.2: Deploy and Test
1. Click **"Deploy"**
2. Wait 5-10 minutes for build completion
3. Test health endpoint:
   ```bash
   curl https://your-faktur-url.railway.app/health
   ```
4. Expected response:
   ```json
   {
     "status": "healthy",
     "service": "faktur-ocr",
     "ocr_engine": "tesseract",
     "version": "1.0.0"
   }
   ```

---

## 🚀 PART 2: DEPLOY BUKTI SETOR SERVICE

### Step 2.1: Create Second Railway Project
1. In Railway dashboard, click **"New Project"** (separate project)
2. Select **"Deploy from GitHub repo"**
3. Choose the SAME repository
4. **IMPORTANT**: Set these configurations:

#### Build Configuration:
```
Root Directory: bukti-setor-service
Dockerfile Path: Dockerfile.bukti-setor
Port: 5002
```

#### Environment Variables (Copy from railway_env_bukti_setor.txt):
```env
DATABASE_URL=postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://hodllrhwyqhrksfkgiqc.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvZGxscmh3eXFocmtzZmtnaXFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjY3NjQyMCwiZXhwIjoyMDUyMjUyNDIwfQ.lAOT5VnU8Kev-aOSDnpG6_Sojsg_SU8-TS1y0YE57Zw
FLASK_ENV=production
FLASK_APP=app_bukti_setor.py
FLASK_DEBUG=false
SECRET_KEY=bukti-setor-production-secret-key-very-secure-32-chars-minimum
PORT=5002
SERVICE_NAME=bukti-setor-ocr-service
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=60
OCR_MAX_RETRIES=3
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=INFO
```

### Step 2.2: Deploy and Test
1. Click **"Deploy"**
2. ⚠️ **IMPORTANT**: Wait 10-15 minutes (EasyOCR models download)
3. Test health endpoint:
   ```bash
   curl https://your-bukti-setor-url.railway.app/health
   ```
4. Expected response:
   ```json
   {
     "status": "healthy",
     "service": "bukti-setor-ocr",
     "ocr_engine": "easyocr",
     "version": "1.0.0"
   }
   ```

---

## 🧪 PART 3: TEST BOTH SERVICES

### Test Faktur Service:
```bash
# Health check
curl https://your-faktur-url.railway.app/health

# Get history (should return empty array initially)
curl https://your-faktur-url.railway.app/api/faktur/history/masukan
```

### Test Bukti Setor Service:
```bash
# Health check
curl https://your-bukti-setor-url.railway.app/health

# Service info
curl https://your-bukti-setor-url.railway.app/api/info

# Get history (should return empty array initially)
curl https://your-bukti-setor-url.railway.app/api/bukti-setor/history
```

---

## 🎯 SUCCESS CHECKLIST

### ✅ Deployment Success When:
- [ ] Faktur Service deployed without errors
- [ ] Bukti Setor Service deployed without errors
- [ ] Both health checks return 200 OK
- [ ] Both services connect to Supabase database
- [ ] API endpoints respond correctly
- [ ] Railway logs show no connection errors

---

## 🎊 FINAL STEP: UPDATE DOCUMENTATION

After successful deployment, you'll have URLs like:
```
Faktur Service: https://faktur-service-production.up.railway.app
Bukti Setor Service: https://bukti-setor-service-production.up.railway.app
```

Update these URLs in your API documentation and share with your team!

---

## 🆘 TROUBLESHOOTING

### If deployment fails:
1. Check Railway build logs
2. Verify environment variables
3. Ensure Dockerfile paths are correct
4. Check GitHub repo has latest code

### Need help?
Just let me know the error message and I'll help troubleshoot! 🚀
