# 🗄️ DATABASE STRATEGY FOR SEPARATED SERVICES

## 🎯 RECOMMENDED APPROACH: SHARED SUPABASE DATABASE

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐        ┌─────────────────┐            │
│  │ FAKTUR SERVICE  │        │BUKTI SETOR SVC  │            │
│  │                 │        │                 │            │
│  │ Railway Project │        │ Railway Project │            │
│  │ Port: 5001      │        │ Port: 5002      │            │
│  │                 │        │                 │            │
│  └─────────┬───────┘        └─────────┬───────┘            │
│            │                          │                     │
│            └─────────┬──────────────────┘                   │
│                      │                                      │
│               ┌──────▼──────┐                               │
│               │   SUPABASE  │                               │
│               │  DATABASE   │                               │
│               │             │                               │
│               │ ┌─────────┐ │                               │
│               │ │ppn_     │ │                               │
│               │ │masukan  │ │                               │
│               │ └─────────┘ │                               │
│               │ ┌─────────┐ │                               │
│               │ │ppn_     │ │                               │
│               │ │keluaran │ │                               │
│               │ └─────────┘ │                               │
│               │ ┌─────────┐ │                               │
│               │ │bukti_   │ │                               │
│               │ │setor    │ │                               │
│               │ └─────────┘ │                               │
│               └─────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

## ✅ ADVANTAGES OF SHARED DATABASE

### 🎯 Single Source of Truth:
- **Consistent Data** - Semua data di satu tempat
- **No Data Sync Issues** - Tidak ada masalah sinkronisasi
- **Unified Reporting** - Mudah membuat laporan gabungan
- **Cost Effective** - Hanya bayar satu database

### 🔧 Easy Management:
- **Single Backup** - Backup hanya satu database
- **Unified Schema** - Schema database terpusat
- **Simple Monitoring** - Monitor satu database saja
- **Easier Maintenance** - Maintenance terpusat

## 🔐 DATABASE CONFIGURATION

### Environment Variables (SAME for both services):
```env
# Both services use the SAME database URL
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres

# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📊 TABLE STRUCTURE IN SUPABASE

### Tables Used by Each Service:

#### Faktur Service Tables:
```sql
-- ppn_masukan (PPN Input/Masukan)
CREATE TABLE ppn_masukan (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(20) NOT NULL,
    tanggal DATE NOT NULL,
    keterangan TEXT,
    npwp_lawan_transaksi VARCHAR(100) NOT NULL,
    nama_lawan_transaksi VARCHAR(255) NOT NULL,
    no_faktur VARCHAR(100) UNIQUE NOT NULL,
    dpp DECIMAL(15,2) NOT NULL,
    ppn DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ppn_keluaran (PPN Output/Keluaran)
CREATE TABLE ppn_keluaran (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(20) NOT NULL,
    tanggal DATE NOT NULL,
    keterangan TEXT,
    npwp_lawan_transaksi VARCHAR(100) NOT NULL,
    nama_lawan_transaksi VARCHAR(255) NOT NULL,
    no_faktur VARCHAR(100) UNIQUE NOT NULL,
    dpp DECIMAL(15,2) NOT NULL,
    ppn DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Bukti Setor Service Table:
```sql
-- bukti_setor (Tax Payment Receipts)
CREATE TABLE bukti_setor (
    id SERIAL PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_setor VARCHAR(100) NOT NULL,
    jumlah DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 IMPLEMENTATION STEPS

### Step 1: Setup Supabase Database
1. Login to Supabase
2. Create new project
3. Create tables using SQL Editor
4. Get connection string

### Step 2: Configure Both Services
- Use SAME `DATABASE_URL` in both services
- Each service only interacts with its relevant tables
- No cross-table operations needed

### Step 3: Deploy Services Separately
```bash
# Deploy Faktur Service
cd faktur-service/
# Deploy to Railway

# Deploy Bukti Setor Service  
cd bukti-setor-service/
# Deploy to Railway
```

## 🔒 SECURITY CONSIDERATIONS

### Row Level Security (RLS):
```sql
-- Optional: Enable RLS for additional security
ALTER TABLE ppn_masukan ENABLE ROW LEVEL SECURITY;
ALTER TABLE ppn_keluaran ENABLE ROW LEVEL SECURITY;
ALTER TABLE bukti_setor ENABLE ROW LEVEL SECURITY;

-- Create policies if needed (basic example)
CREATE POLICY "Enable read access for all users" ON ppn_masukan FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON ppn_masukan FOR INSERT WITH CHECK (true);
```

### Connection Security:
- Use SSL connections (default with Supabase)
- Store credentials in environment variables
- Use connection pooling

## 💡 ALTERNATIVE OPTIONS (NOT RECOMMENDED for your case)

### Option B: Separate Databases
```
Faktur Service → Supabase Database A
Bukti Setor Service → Supabase Database B
```
**Cons:** More complex, higher cost, data sync issues

### Option C: Database per Service + Sync
```
Each service has its own DB + sync mechanism
```
**Cons:** Much more complex, potential sync failures

## 🎯 CONCLUSION

**BEST CHOICE: Shared Supabase Database**
- ✅ Simple to implement
- ✅ Cost effective  
- ✅ No data sync issues
- ✅ Easy to maintain
- ✅ Perfect for your use case

Each service is independent but uses the same database connection, accessing only their relevant tables.
