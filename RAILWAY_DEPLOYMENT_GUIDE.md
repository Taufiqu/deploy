# 🚂 RAILWAY DEPLOYMENT GUIDE - SEPARATED SERVICES

## 📋 PREREQUISITES CHECKLIST

Before deploying, ensure you have:
- ✅ Supabase database setup completed
- ✅ Database credentials ready
- ✅ GitHub repository with the code
- ✅ Railway account connected to GitHub

---

## 🚀 PART 1: DEPLOY FAKTUR SERVICE

### Step 1.1: Create Railway Project for Faktur
1. Login to [Railway](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Configure deployment:

#### Build Settings:
```yaml
Root Directory: faktur-service
Build Command: docker build -f Dockerfile.faktur -t faktur-service .
Start Command: [from Dockerfile]
Port: 5001
```

#### Environment Variables:
```env
# Database (REPLACE with your actual Supabase values)
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here

# Application
FLASK_ENV=production
FLASK_APP=app_faktur.py
SECRET_KEY=your-production-secret-key-change-this
PORT=5001

# OCR Settings
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=30
OCR_MAX_RETRIES=3
MAX_CONTENT_LENGTH=16777216

# Service Info
SERVICE_NAME=faktur-ocr-service
LOG_LEVEL=INFO
```

### Step 1.2: Deploy Faktur Service
1. Click "Deploy"
2. Wait for build completion (5-10 minutes)
3. Test deployment:
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

### Step 2.1: Create Railway Project for Bukti Setor
1. In Railway dashboard, click "New Project" (separate project)
2. Select "Deploy from GitHub repo"
3. Choose the same repository
4. Configure deployment:

#### Build Settings:
```yaml
Root Directory: bukti-setor-service
Build Command: docker build -f Dockerfile.bukti-setor -t bukti-setor-service .
Start Command: [from Dockerfile]
Port: 5002
```

#### Environment Variables:
```env
# Database (SAME as Faktur Service - shared database)
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here

# Application
FLASK_ENV=production
FLASK_APP=app_bukti_setor.py
SECRET_KEY=your-production-secret-key-change-this
PORT=5002

# OCR Settings
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=60
OCR_MAX_RETRIES=3
MAX_CONTENT_LENGTH=16777216
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR

# Service Info
SERVICE_NAME=bukti-setor-ocr-service
LOG_LEVEL=INFO
```

### Step 2.2: Deploy Bukti Setor Service
1. Click "Deploy"
2. Wait for build completion (10-15 minutes - EasyOCR models download)
3. Test deployment:
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

### Test Faktur Service APIs:
```bash
# Health check
curl https://your-faktur-url.railway.app/health

# Get history
curl https://your-faktur-url.railway.app/api/faktur/history/masukan

# Upload test (with file)
curl -X POST \
  https://your-faktur-url.railway.app/api/faktur/upload \
  -F "file=@test-invoice.pdf" \
  -F "jenis_pajak=masukan"
```

### Test Bukti Setor Service APIs:
```bash
# Health check  
curl https://your-bukti-setor-url.railway.app/health

# Service info
curl https://your-bukti-setor-url.railway.app/api/info

# Get history
curl https://your-bukti-setor-url.railway.app/api/bukti-setor/history

# Upload test (with file)
curl -X POST \
  https://your-bukti-setor-url.railway.app/api/bukti-setor/upload \
  -F "file=@test-receipt.pdf"
```

---

## 📊 PART 4: VERIFY DATABASE CONNECTION

### Check Database Tables in Supabase:
1. Go to Supabase → Table Editor
2. Verify data is being saved:
   - Check `ppn_masukan` table for faktur uploads
   - Check `bukti_setor` table for receipt uploads

### Monitor Railway Logs:
1. In Railway dashboard → Your service → Logs
2. Look for successful database connections:
   ```
   Database connection successful
   Tables created/updated
   OCR processing completed
   ```

---

## 🎯 PART 5: PRODUCTION CONFIGURATION

### Custom Domains (Optional):
1. In Railway project settings
2. Add custom domain
3. Update DNS records

### Environment Variables Best Practices:
```env
# Use strong secrets in production
SECRET_KEY=$(openssl rand -hex 32)

# Monitor resource usage
LOG_LEVEL=INFO

# Optimize for production
FLASK_ENV=production
FLASK_DEBUG=false
```

### Resource Monitoring:
- Monitor memory usage (EasyOCR uses ~2GB)
- Check response times
- Monitor database connections

---

## ✅ DEPLOYMENT SUCCESS CHECKLIST

### Before Going Live:
- [ ] Both services deploy successfully
- [ ] Health checks return 200 OK
- [ ] Database connection working
- [ ] File uploads functional
- [ ] OCR processing working
- [ ] API endpoints responding

### After Deployment:
- [ ] Update API documentation with production URLs
- [ ] Set up monitoring/alerts
- [ ] Configure backup strategy
- [ ] Update frontend to use production endpoints

---

## 🆘 TROUBLESHOOTING

### Common Issues:

#### Build Failures:
```bash
# Check Dockerfile syntax
# Verify requirements.txt
# Check Railway build logs
```

#### Memory Issues:
```bash
# EasyOCR service needs more RAM
# Upgrade Railway plan if needed
# Monitor resource usage
```

#### Database Connection:
```bash
# Verify DATABASE_URL format
# Check Supabase firewall settings
# Test connection locally first
```

### Debug Commands:
```bash
# Check Railway logs
railway logs --service your-service

# Test endpoints
curl -v https://your-service.railway.app/health

# Check database
psql $DATABASE_URL -c "SELECT COUNT(*) FROM ppn_masukan;"
```

---

## 🎊 SUCCESS!

Once both services are deployed and working:

🎯 **You now have:**
- ✅ Faktur Service running independently
- ✅ Bukti Setor Service running independently  
- ✅ Shared Supabase database
- ✅ Scalable architecture
- ✅ Production-ready deployment

**Your separated OCR services are live! 🚀**
