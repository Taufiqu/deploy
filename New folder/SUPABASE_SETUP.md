# Setup Database Supabase

Panduan untuk mengkonfigurasi proyek ini dengan database Supabase.

## Persiapan

1. **Pastikan Supabase Project sudah dibuat**
   - Login ke [Supabase Dashboard](https://supabase.com/dashboard)
   - Buat project baru atau gunakan project yang sudah ada
   - Catat connection string dari Settings > Database

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Konfigurasi Database

1. **Update file .env**
   - Salin `.env.example` ke `.env` jika belum ada
   - Update `DATABASE_URL` dengan connection string Supabase Anda:
   ```
   DATABASE_URL=postgresql://postgres:your_password@db.your_project_ref.supabase.co:5432/postgres
   ```

2. **Test Koneksi Database**
   Untuk test koneksi, Anda bisa menggunakan aplikasi utama:
   ```bash
   python app.py
   ```

## Menjalankan Aplikasi

1. **Jalankan Aplikasi Langsung**
   ```bash
   python app.py
   ```
   
   Database akan otomatis diinisialisasi saat aplikasi pertama kali dijalankan.

## Troubleshooting

### Error: SSL Connection Required
Pastikan `sslmode=require` sudah dikonfigurasi di `config.py`. Supabase memerlukan SSL connection.

### Error: Authentication Failed
Periksa kembali password dan connection string di file `.env`.

### Error: Table Not Found
Periksa file `models.py` dan pastikan semua tabel sudah didefinisikan dengan benar. Aplikasi akan membuat tabel secara otomatis saat pertama kali dijalankan.

## Migrasi Data (Opsional)

Jika Anda memiliki data di database lokal dan ingin migrasi ke Supabase:

1. Export data dari database lokal
2. Update connection string ke Supabase
3. Import data ke Supabase

## File Penting

- `config.py` - Konfigurasi database dan SSL
- `models.py` - Schema database
- `app.py` - Aplikasi utama

## Support

Jika mengalami masalah, periksa:
1. Connection string sudah benar
2. Password Supabase sudah benar
3. SSL configuration sudah aktif
4. Network bisa akses ke Supabase (tidak diblokir firewall)
