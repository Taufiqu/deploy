# ✅ RAILWAY DEPLOYMENT CHECKLIST

## 🎯 PRE-DEPLOYMENT (DO THESE FIRST)

### ☑️ Supabase Setup
- [ ] Created Supabase project
- [ ] Ran `supabase_setup.sql` in SQL Editor
- [ ] Verified tables created: `ppn_masukan`, `ppn_keluaran`, `bukti_setor`
- [ ] Got DATABASE_URL from Settings → Database
- [ ] Got SUPABASE_URL and ANON_KEY from Settings → API

### ☑️ GitHub Repository
- [ ] Code pushed to GitHub
- [ ] Repository is public or Railway has access
- [ ] Both service directories exist: `faktur-service/` and `bukti-setor-service/`

---

## 🚂 RAILWAY DEPLOYMENT

### ☑️ Deploy Faktur Service (First)
- [ ] Created new Railway project
- [ ] Connected to GitHub repository
- [ ] Set Root Directory: `faktur-service`
- [ ] Environment variables configured (see below)
- [ ] Deployment successful
- [ ] Health check responds: `curl https://faktur-url/health`

#### Faktur Service Environment Variables:
```env
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
FLASK_ENV=production
FLASK_APP=app_faktur.py
SECRET_KEY=your-very-secure-secret-key-minimum-32-chars
PORT=5001
SERVICE_NAME=faktur-ocr-service
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=30
OCR_MAX_RETRIES=3
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=INFO
```

### ☑️ Deploy Bukti Setor Service (Second)
- [ ] Created second Railway project (separate from faktur)
- [ ] Connected to same GitHub repository
- [ ] Set Root Directory: `bukti-setor-service`
- [ ] Environment variables configured (see below)
- [ ] Deployment successful (takes 10-15 minutes)
- [ ] Health check responds: `curl https://bukti-setor-url/health`

#### Bukti Setor Service Environment Variables:
```env
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
FLASK_ENV=production
FLASK_APP=app_bukti_setor.py
SECRET_KEY=your-very-secure-secret-key-minimum-32-chars
PORT=5002
SERVICE_NAME=bukti-setor-ocr-service
POPPLER_PATH=/usr/bin
OCR_TIMEOUT=60
OCR_MAX_RETRIES=3
MAX_CONTENT_LENGTH=16777216
EASYOCR_MODULE_PATH=/home/appuser/.EasyOCR
LOG_LEVEL=INFO
```

---

## 🧪 POST-DEPLOYMENT TESTING

### ☑️ Test Faktur Service
- [ ] Health check: `GET /health`
- [ ] Service info shows Tesseract OCR
- [ ] History endpoint: `GET /api/faktur/history/masukan`
- [ ] Upload test file (optional)

### ☑️ Test Bukti Setor Service  
- [ ] Health check: `GET /health`
- [ ] Service info: `GET /api/info` shows EasyOCR
- [ ] History endpoint: `GET /api/bukti-setor/history`
- [ ] Upload test file (optional)

### ☑️ Test Database Integration
- [ ] Supabase tables receive data from uploads
- [ ] Both services connect to same database
- [ ] No connection errors in Railway logs

---

## 📝 DEPLOYMENT URLS

After successful deployment, update these:

### Production URLs:
```
Faktur Service: https://faktur-service-production.up.railway.app
Bukti Setor Service: https://bukti-setor-service-production.up.railway.app
```

### Update Documentation:
- [ ] Update `API_DOCS_SEPARATED.md` with production URLs
- [ ] Share URLs with frontend team/users
- [ ] Test all endpoints with production URLs

---

## 🎊 SUCCESS CRITERIA

### ✅ Deployment is successful when:
1. **Both Railway projects deployed without errors**
2. **Health checks return 200 OK**
3. **Database connections working**  
4. **OCR processing functional**
5. **File uploads working**
6. **API endpoints responding correctly**

### 🔍 Monitoring Setup:
- [ ] Railway dashboard shows services running
- [ ] Check Railway logs for any errors
- [ ] Monitor resource usage (especially bukti-setor service)
- [ ] Set up uptime monitoring (optional)

---

## 🆘 TROUBLESHOOTING QUICK FIXES

### If Deployment Fails:
1. **Check Railway build logs** for specific errors
2. **Verify Dockerfile syntax** and file paths
3. **Check environment variables** are set correctly
4. **Ensure GitHub repo has latest code**

### If Health Check Fails:
1. **Check Railway logs** for application errors
2. **Verify DATABASE_URL** connection
3. **Check port configuration** (5001/5002)
4. **Test locally** with same environment

### If Database Connection Fails:
1. **Verify Supabase DATABASE_URL** format
2. **Check Supabase dashboard** for connection issues
3. **Test connection** from local machine
4. **Ensure tables exist** in Supabase

---

## 🎯 FINAL CHECKLIST

Before marking deployment as complete:

- [ ] ✅ Supabase database setup and working
- [ ] ✅ Faktur Service deployed and responding
- [ ] ✅ Bukti Setor Service deployed and responding  
- [ ] ✅ Both services connect to same database
- [ ] ✅ API endpoints tested and working
- [ ] ✅ Documentation updated with production URLs
- [ ] ✅ Team notified of new service URLs

**🎉 CONGRATULATIONS! Your separated OCR services are now live on Railway! 🚀**
