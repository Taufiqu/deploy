# 🚀 DEPLOYMENT GUIDE - SEPARATED SERVICES

## 📋 PREREQUISITES

### 1. Supabase Setup
1. Login to [Supabase](https://supabase.com/)
2. Create a new project
3. Go to SQL Editor
4. Run the SQL script: `supabase_setup.sql`
5. Get your database credentials:
   - Project URL
   - Database URL
   - Anon Key

### 2. Railway Account
1. Login to [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Prepare to create 2 separate projects

---

## 🛠️ STEP-BY-STEP DEPLOYMENT

### Step 1: Setup Environment Variables

#### Get Supabase Credentials:
```bash
# From Supabase Dashboard > Settings > Database
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres

# From Supabase Dashboard > Settings > API
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Step 2: Deploy Faktur Service

#### 2.1 Create Railway Project for Faktur Service
```bash
# In Railway Dashboard:
1. Create New Project
2. Deploy from GitHub repo
3. Set root directory: /faktur-service
4. Use Dockerfile.faktur
```

#### 2.2 Set Environment Variables in Railway:
```env
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key
FLASK_ENV=production
FLASK_APP=app_faktur.py
PORT=5001
```

#### 2.3 Configure Build Settings:
```
Root Directory: /faktur-service
Dockerfile Path: Dockerfile.faktur
Build Command: (automatic from Dockerfile)
Start Command: (automatic from Dockerfile)
```

### Step 3: Deploy Bukti Setor Service

#### 3.1 Create Railway Project for Bukti Setor Service
```bash
# In Railway Dashboard:
1. Create New Project (separate from faktur)
2. Deploy from GitHub repo
3. Set root directory: /bukti-setor-service
4. Use Dockerfile.bukti-setor
```

#### 3.2 Set Environment Variables in Railway:
```env
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key
FLASK_ENV=production
FLASK_APP=app_bukti_setor.py
PORT=5002
```

#### 3.3 Configure Build Settings:
```
Root Directory: /bukti-setor-service
Dockerfile Path: Dockerfile.bukti-setor
Build Command: (automatic from Dockerfile)
Start Command: (automatic from Dockerfile)
```

---

## 🧪 LOCAL TESTING BEFORE DEPLOYMENT

### Test Database Connection

#### Test Faktur Service:
```bash
cd faktur-service
python test_db_connection.py
```

#### Test Bukti Setor Service:
```bash
cd bukti-setor-service
python test_db_connection.py
```

### Test Docker Builds

#### Build Faktur Service:
```bash
cd faktur-service
docker build -f Dockerfile.faktur -t faktur-service .
docker run -p 5001:5001 --env-file .env faktur-service
```

#### Build Bukti Setor Service:
```bash
cd bukti-setor-service
docker build -f Dockerfile.bukti-setor -t bukti-setor-service .
docker run -p 5002:5002 --env-file .env bukti-setor-service
```

### Test APIs

#### Test Faktur Service:
```bash
curl http://localhost:5001/health
curl http://localhost:5001/api/faktur/history/masukan
```

#### Test Bukti Setor Service:
```bash
curl http://localhost:5002/health
curl http://localhost:5002/api/info
curl http://localhost:5002/api/bukti-setor/history
```

---

## 🌐 POST-DEPLOYMENT

### Get Deployment URLs
After successful deployment, you'll get URLs like:
- **Faktur Service**: `https://faktur-service-production.up.railway.app`
- **Bukti Setor Service**: `https://bukti-setor-service-production.up.railway.app`

### Test Production APIs
```bash
# Test Faktur Service
curl https://your-faktur-url.railway.app/health

# Test Bukti Setor Service
curl https://your-bukti-setor-url.railway.app/health
```

### Update API Documentation
Update `API_DOCS_SEPARATED.md` with actual production URLs.

---

## 🔧 TROUBLESHOOTING

### Common Issues:

#### Database Connection Failed
```bash
# Check if DATABASE_URL is correct
# Verify Supabase is accessible
# Check firewall settings
```

#### Docker Build Failed
```bash
# Check Dockerfile syntax
# Verify requirements.txt
# Check if all files are copied correctly
```

#### Service Not Starting
```bash
# Check environment variables
# Verify port configuration
# Check application logs in Railway dashboard
```

### Debug Commands:
```bash
# Check Railway logs
railway logs

# Test database connection locally
python test_db_connection.py

# Verify Docker build
docker build -f Dockerfile.faktur -t test-faktur .
```

---

## ✅ VERIFICATION CHECKLIST

### Before Deployment:
- [ ] Supabase database setup completed
- [ ] Tables created successfully
- [ ] Local database connection test passed
- [ ] Docker builds successful locally
- [ ] Environment variables configured

### After Deployment:
- [ ] Both services deployed successfully
- [ ] Health checks return 200 OK
- [ ] Database connection working in production
- [ ] API endpoints responding correctly
- [ ] File uploads working
- [ ] OCR processing functional

---

## 🎯 NEXT STEPS

1. **Monitor Performance**: Check Railway metrics
2. **Set Up Monitoring**: Configure error tracking
3. **Scale if Needed**: Adjust Railway plan based on usage
4. **Backup Strategy**: Ensure Supabase backups are enabled
5. **Custom Domain**: Configure custom domains if needed

## 🆘 SUPPORT

If you encounter issues:
1. Check Railway deployment logs
2. Verify Supabase connection
3. Test locally first
4. Check environment variables
5. Review this deployment guide
