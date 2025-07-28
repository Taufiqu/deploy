# 🗄️ SUPABASE SETUP GUIDE - STEP BY STEP

## 📋 STEP 1: CREATE SUPABASE PROJECT

### 1.1 Login to Supabase
1. Go to [https://supabase.com/](https://supabase.com/)
2. Click "Start your project"
3. Sign in with GitHub/Google/Email

### 1.2 Create New Project
1. Click "New Project"
2. Choose your organization
3. Fill in project details:
   ```
   Name: ocr-separated-services
   Database Password: [CREATE A STRONG PASSWORD]
   Region: Southeast Asia (Singapore) [or closest to you]
   ```
4. Click "Create new project"
5. Wait 2-3 minutes for setup

---

## 📊 STEP 2: SETUP DATABASE TABLES

### 2.1 Open SQL Editor
1. In Supabase dashboard, go to "SQL Editor"
2. Click "New query"
3. Copy and paste the content from `supabase_setup.sql`
4. Click "Run" to execute

### 2.2 Verify Tables Created
After running the SQL, verify in "Table Editor":
- ✅ `ppn_masukan` table
- ✅ `ppn_keluaran` table  
- ✅ `bukti_setor` table

---

## 🔑 STEP 3: GET DATABASE CREDENTIALS

### 3.1 Get Database URL
1. Go to "Settings" → "Database"
2. Scroll down to "Connection string"
3. Copy the "URI" connection string:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.co:5432/postgres
   ```

### 3.2 Get API Credentials (Optional)
1. Go to "Settings" → "API"
2. Copy these values:
   ```
   Project URL: https://xxxxx.supabase.co
   Anon Key: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   ```

---

## ✅ STEP 4: UPDATE ENVIRONMENT FILES

### 4.1 Update Faktur Service
Edit `faktur-service/.env.example`:
```env
DATABASE_URL=postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

### 4.2 Update Bukti Setor Service  
Edit `bukti-setor-service/.env.example`:
```env
DATABASE_URL=postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

---

## 🧪 STEP 5: TEST CONNECTION (OPTIONAL)

If you want to test locally:
1. Create `.env` file in service directory
2. Copy credentials from `.env.example`
3. Install psycopg2: `pip install psycopg2-binary`
4. Run: `python test_db_connection.py`

---

## 📤 READY FOR RAILWAY DEPLOYMENT

Once Supabase is setup:
1. ✅ Database tables created
2. ✅ Credentials obtained
3. ✅ Environment files updated
4. ✅ Ready for Railway deployment

**Next: Deploy to Railway with these credentials!**
