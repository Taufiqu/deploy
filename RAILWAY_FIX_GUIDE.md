# 🚀 RAILWAY DEPLOYMENT GUIDE - FAKTUR SERVICE
# ===================================================

## ❌ MASALAH YANG KAMU ALAMI:
```
Nixpacks build failed
Nixpacks was unable to generate a build plan for this app.
```

## ✅ SOLUSI YANG SUDAH DIPERBAIKI:

### 1. File Standar Railway Sudah Dibuat:
- ✅ `requirements.txt` (Railway standard)
- ✅ `Dockerfile` (Railway standard)  
- ✅ `Procfile` (Railway standard)
- ✅ `nixpacks.toml` (Force Dockerfile build)
- ✅ `railway.json` (Railway config)

### 2. Health Endpoint Sudah Ada:
- ✅ `/health` endpoint di `app_faktur.py`

## 🔧 LANGKAH DEPLOY DI RAILWAY:

### Step 1: Login ke Railway
1. Buka https://railway.app
2. Login dengan GitHub account
3. Connect ke repository `deploy`

### Step 2: Create New Project
1. Klik "New Project"
2. Pilih "Deploy from GitHub repo"
3. Pilih repository: `Taufiqu/deploy`

### Step 3: Configure Service Root
⚠️ **PENTING**: Saat deploy, Railway akan scan seluruh repository.
Kamu harus set **Root Directory**:

1. Setelah select repo, klik "Configure"
2. Set **Root Directory**: `faktur-service`
3. Klik "Deploy"

### Step 4: Environment Variables
Tambahkan environment variables ini di Railway dashboard:

```
DATABASE_URL=postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://hodllrhwyqhrksfkgiqc.supabase.co
FLASK_ENV=production
SECRET_KEY=your-production-secret-key-here
```

### Step 5: Build Configuration
Railway akan otomatis detect:
- ✅ `Dockerfile` untuk build
- ✅ `requirements.txt` untuk dependencies
- ✅ Port dari Dockerfile (5001)

## 🎯 TROUBLESHOOTING:

### Jika Masih Error "Nixpacks build failed":
1. **Pastikan Root Directory benar**: `faktur-service`
2. **Force rebuild**: Klik "Deploy" > "Redeploy"
3. **Check logs**: Railway dashboard > "Deployments" > "View Logs"

### Jika Build Success tapi App Crash:
1. Check **Environment Variables** sudah benar
2. Check **Database connection** via logs
3. Check **Port binding** (Railway auto-set $PORT)

## 📱 TESTING DEPLOYMENT:

Setelah deploy success, kamu akan dapat URL seperti:
```
https://faktur-service-production-xxxx.up.railway.app
```

Test endpoints:
- ✅ `GET /health` - Health check
- ✅ `POST /process-invoice` - Upload faktur
- ✅ `GET /history` - Get invoice history

## 🔄 DEPLOY BUKTI SETOR SERVICE:

Repeat langkah yang sama untuk bukti-setor:
1. Create new project di Railway
2. Set **Root Directory**: `bukti-setor-service`
3. Add same environment variables
4. Deploy

## 🎉 HASIL AKHIR:
- 🧾 Faktur Service: `https://faktur-xxxx.up.railway.app`
- 🧾 Bukti Setor Service: `https://bukti-setor-xxxx.up.railway.app`
- 🗄️ Shared Database: Supabase PostgreSQL

---
**✨ Coba deploy lagi dengan setting Root Directory = `faktur-service`**
