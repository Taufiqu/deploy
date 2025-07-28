-- ========================================
-- SUPABASE DATABASE SETUP
-- SHARED DATABASE FOR SEPARATED SERVICES
-- ========================================

-- Run this in Supabase SQL Editor to create tables

-- ========================================
-- FAKTUR SERVICE TABLES
-- ========================================

-- Table for PPN Masukan (Input Tax)
CREATE TABLE IF NOT EXISTS ppn_masukan (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(20) NOT NULL,
    tanggal DATE NOT NULL,
    keterangan TEXT,
    npwp_lawan_transaksi VARCHAR(100) NOT NULL,
    nama_lawan_transaksi VARCHAR(255) NOT NULL,
    no_faktur VARCHAR(100) UNIQUE NOT NULL,
    dpp DECIMAL(15,2) NOT NULL,
    ppn DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for PPN Keluaran (Output Tax)
CREATE TABLE IF NOT EXISTS ppn_keluaran (
    id SERIAL PRIMARY KEY,
    bulan VARCHAR(20) NOT NULL,
    tanggal DATE NOT NULL,
    keterangan TEXT,
    npwp_lawan_transaksi VARCHAR(100) NOT NULL,
    nama_lawan_transaksi VARCHAR(255) NOT NULL,
    no_faktur VARCHAR(100) UNIQUE NOT NULL,
    dpp DECIMAL(15,2) NOT NULL,
    ppn DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- BUKTI SETOR SERVICE TABLE
-- ========================================

-- Table for Bukti Setor (Tax Payment Receipts)
CREATE TABLE IF NOT EXISTS bukti_setor (
    id SERIAL PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_setor VARCHAR(100) NOT NULL,
    jumlah DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- INDEXES FOR PERFORMANCE
-- ========================================

-- Indexes for ppn_masukan
CREATE INDEX IF NOT EXISTS idx_ppn_masukan_tanggal ON ppn_masukan(tanggal);
CREATE INDEX IF NOT EXISTS idx_ppn_masukan_no_faktur ON ppn_masukan(no_faktur);
CREATE INDEX IF NOT EXISTS idx_ppn_masukan_created_at ON ppn_masukan(created_at);

-- Indexes for ppn_keluaran
CREATE INDEX IF NOT EXISTS idx_ppn_keluaran_tanggal ON ppn_keluaran(tanggal);
CREATE INDEX IF NOT EXISTS idx_ppn_keluaran_no_faktur ON ppn_keluaran(no_faktur);
CREATE INDEX IF NOT EXISTS idx_ppn_keluaran_created_at ON ppn_keluaran(created_at);

-- Indexes for bukti_setor
CREATE INDEX IF NOT EXISTS idx_bukti_setor_tanggal ON bukti_setor(tanggal);
CREATE INDEX IF NOT EXISTS idx_bukti_setor_kode_setor ON bukti_setor(kode_setor);
CREATE INDEX IF NOT EXISTS idx_bukti_setor_created_at ON bukti_setor(created_at);

-- ========================================
-- ROW LEVEL SECURITY (OPTIONAL)
-- ========================================

-- Enable RLS for additional security (optional)
-- ALTER TABLE ppn_masukan ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE ppn_keluaran ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE bukti_setor ENABLE ROW LEVEL SECURITY;

-- Create policies for read/write access (if RLS enabled)
-- CREATE POLICY "Enable read access for all users" ON ppn_masukan FOR SELECT USING (true);
-- CREATE POLICY "Enable insert access for all users" ON ppn_masukan FOR INSERT WITH CHECK (true);
-- CREATE POLICY "Enable update access for all users" ON ppn_masukan FOR UPDATE USING (true);
-- CREATE POLICY "Enable delete access for all users" ON ppn_masukan FOR DELETE USING (true);

-- Repeat for other tables...

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- Check if tables are created successfully
SELECT table_name, table_schema 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('ppn_masukan', 'ppn_keluaran', 'bukti_setor')
ORDER BY table_name;

-- Check table structures
\d ppn_masukan;
\d ppn_keluaran;
\d bukti_setor;

-- ========================================
-- SAMPLE DATA (OPTIONAL FOR TESTING)
-- ========================================

-- Insert sample data for testing (optional)
/*
INSERT INTO ppn_masukan (bulan, tanggal, keterangan, npwp_lawan_transaksi, nama_lawan_transaksi, no_faktur, dpp, ppn)
VALUES 
    ('Januari', '2024-01-15', 'Pembelian barang', '12.345.678.9-012.000', 'PT CONTOH PERUSAHAAN', '010.000-24.00000001', 1000000.00, 110000.00),
    ('Januari', '2024-01-20', 'Jasa konsultasi', '98.765.432.1-098.000', 'CV MITRA SEJAHTERA', '010.000-24.00000002', 5000000.00, 550000.00);

INSERT INTO ppn_keluaran (bulan, tanggal, keterangan, npwp_lawan_transaksi, nama_lawan_transaksi, no_faktur, dpp, ppn)
VALUES 
    ('Januari', '2024-01-16', 'Penjualan produk', '11.222.333.4-567.000', 'PT PEMBELI SETIA', '020.000-24.00000001', 2000000.00, 220000.00);

INSERT INTO bukti_setor (tanggal, kode_setor, jumlah)
VALUES 
    ('2024-01-25', '411128', 500000.00),
    ('2024-01-30', '411211', 300000.00);
*/

-- ========================================
-- SUCCESS MESSAGE
-- ========================================

SELECT 'Database setup completed successfully! Ready for Railway deployment.' AS status;
