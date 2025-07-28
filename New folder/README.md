# 📄 Proyek Pajak Backend - OCR Invoice Processing

Sistem backend untuk pemrosesan dokumen pajak menggunakan OCR (Optical Character Recognition) dengan Flask dan Supabase.

## 🚀 Fitur Utama

- **OCR Processing**: Ekstraksi data dari faktur pajak dan bukti setor secara otomatis
- **Database Integration**: Penyimpanan data dengan PostgreSQL (Supabase)
- **RESTful API**: Endpoint untuk upload, process, dan export data
- **Excel Export**: Generate laporan dalam format Excel
- **Multi-format Support**: Support untuk PDF dan gambar (JPG, PNG)
- **Spell Check**: Koreksi otomatis untuk hasil OCR
- **Data Validation**: Validasi format nomor faktur dan tanggal

## 📋 Daftar Isi

- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## 🔧 Installation

### Prerequisites

- Python 3.8 atau lebih tinggi
- PostgreSQL database (Supabase)
- Poppler (untuk PDF processing)

### 1. Clone Repository

```bash
git clone https://github.com/Taufiqu/proyek-pajak-backend-clean.git
cd proyek-pajak-backend-clean
```

### 2. Setup Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Poppler

**Windows:**
1. Download Poppler dari [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract ke `C:\poppler\`
3. Update `POPPLER_PATH` di `.env`

**Linux:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

## ⚙️ Configuration

### 1. Environment Variables

Salin file `.env.example` ke `.env` dan sesuaikan:

```bash
cp .env.example .env
```

### 2. Database Setup

Update file `.env` dengan kredensial Supabase:

```properties
# Database connection string untuk Supabase
DATABASE_URL="postgresql://postgres.username:password@host:5432/postgres"

# Konfigurasi Supabase lengkap
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Konfigurasi aplikasi
FLASK_PORT=5001

# Pengaturan Spesifik Lingkungan
POPPLER_PATH="C:\\poppler\\poppler-24.08.0\\Library\\bin"
```

### 3. Database Migration

```bash
# Inisialisasi database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 🚀 Running the Application

```bash
# Aktivasi virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Jalankan aplikasi
python app.py
```

Server akan berjalan di `http://localhost:5001`

## 📚 API Documentation

### Faktur Pajak Endpoints

#### 1. Process Invoice File

```http
POST /api/process
Content-Type: multipart/form-data

Parameters:
- file: File (PDF/Image)
- jenis: string ("masukan" | "keluaran")
```

**Response:**
```json
{
  "success": true,
  "data": {
    "no_faktur": "010.000-24.00000001",
    "tanggal": "2024-01-15",
    "nama_lawan_transaksi": "PT. Contoh",
    "npwp_lawan_transaksi": "01.234.567.8-901.000",
    "dpp": 100000,
    "ppn": 11000,
    "keterangan": "Pembelian barang"
  }
}
```

#### 2. Save Invoice Data

```http
POST /api/save
Content-Type: application/json

Body:
{
  "jenis": "masukan",
  "no_faktur": "010.000-24.00000001",
  "tanggal": "2024-01-15",
  "nama_lawan_transaksi": "PT. Contoh",
  "npwp_lawan_transaksi": "01.234.567.8-901.000",
  "dpp": 100000,
  "ppn": 11000,
  "keterangan": "Pembelian barang"
}
```

#### 3. Get History

```http
GET /api/history
```

**Response:**
```json
[
  {
    "id": 1,
    "jenis": "masukan",
    "no_faktur": "010.000-24.00000001",
    "nama_lawan_transaksi": "PT. Contoh",
    "tanggal": "2024-01-15"
  }
]
```

#### 4. Export to Excel

```http
GET /api/export
```

#### 5. Delete Invoice

```http
DELETE /api/delete/{jenis}/{id}
```

### Bukti Setor Endpoints

#### 1. Process Bukti Setor

```http
POST /api/bukti_setor/process
Content-Type: multipart/form-data

Parameters:
- file: File (PDF/Image)
```

#### 2. Save Bukti Setor

```http
POST /api/bukti_setor/save
Content-Type: application/json

Body:
{
  "tanggal": "2024-01-15",
  "kode_setor": "411211",
  "jumlah": 100000
}
```

#### 3. Get History

```http
GET /api/bukti_setor/history
```

#### 4. Export to Excel

```http
GET /api/bukti_setor/export
```

#### 5. Delete Bukti Setor

```http
DELETE /api/bukti_setor/delete/{id}
```

## 🗄️ Database Schema

### Tabel ppn_masukan

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| bulan | VARCHAR(20) | Bulan transaksi |
| tanggal | DATE | Tanggal faktur |
| keterangan | TEXT | Keterangan transaksi |
| npwp_lawan_transaksi | VARCHAR(100) | NPWP lawan transaksi |
| nama_lawan_transaksi | VARCHAR(255) | Nama lawan transaksi |
| no_faktur | VARCHAR(100) | Nomor faktur (unique) |
| dpp | DECIMAL(15,2) | Dasar Pengenaan Pajak |
| ppn | DECIMAL(15,2) | Pajak Pertambahan Nilai |
| created_at | TIMESTAMP | Waktu dibuat |

### Tabel ppn_keluaran

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| bulan | VARCHAR(20) | Bulan transaksi |
| tanggal | DATE | Tanggal faktur |
| keterangan | TEXT | Keterangan transaksi |
| npwp_lawan_transaksi | VARCHAR(100) | NPWP lawan transaksi |
| nama_lawan_transaksi | VARCHAR(255) | Nama lawan transaksi |
| no_faktur | VARCHAR(100) | Nomor faktur (unique) |
| dpp | DECIMAL(15,2) | Dasar Pengenaan Pajak |
| ppn | DECIMAL(15,2) | Pajak Pertambahan Nilai |
| created_at | TIMESTAMP | Waktu dibuat |

### Tabel bukti_setor

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| tanggal | DATE | Tanggal setor |
| kode_setor | VARCHAR(100) | Kode setor pajak |
| jumlah | DECIMAL(15,2) | Jumlah setor |
| created_at | TIMESTAMP | Waktu dibuat |

## 📁 Project Structure

```
proyek-pajak-backend-clean/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .env.example         # Environment variables template
├── Dockerfile           # Docker configuration
├── Procfile             # Heroku deployment
├── bukti_setor/         # Bukti setor module
│   ├── __init__.py
│   ├── routes.py        # Bukti setor routes
│   ├── services/        # Business logic
│   │   ├── delete.py
│   │   └── excel_exporter_bukti_setor.py
│   └── utils/           # Utilities
│       ├── bukti_setor_processor.py
│       ├── ocr_engine.py
│       ├── spellcheck.py
│       └── parsing/     # Data parsing
├── faktur/              # Invoice processing module
│   ├── services/        # Business logic
│   │   ├── delete.py
│   │   ├── excel_exporter.py
│   │   ├── file_saver.py
│   │   ├── history.py
│   │   └── invoice_processor.py
│   └── utils/           # Utilities
│       ├── helpers.py
│       ├── preprocessing.py
│       └── extraction/  # Data extraction
├── shared_utils/        # Shared utilities
│   ├── file_utils.py
│   └── text_utils.py
├── migrations/          # Database migrations
├── templates/           # Excel templates
├── uploads/             # File uploads
└── venv/               # Virtual environment
```

## 🔧 Development

### Running Tests

```bash
# Placeholder for future test implementation
python -m pytest tests/
```

### Code Style

Project menggunakan:
- **Black** untuk formatting
- **isort** untuk import sorting
- **flake8** untuk linting

```bash
# Format code
black .
isort .

# Lint code
flake8 .
```

### Adding New Features

1. **OCR Processing**: Extend `bukti_setor/utils/ocr_engine.py`
2. **Data Validation**: Add validators in `shared_utils/`
3. **API Endpoints**: Add routes in respective modules
4. **Database Models**: Extend `models.py`

## 📊 Monitoring & Logging

### Logging Configuration

Application menggunakan Python logging untuk tracking:
- OCR processing status
- Database operations
- API requests/responses
- Error tracking

### Health Check

```http
GET /api/health
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: Address already in use
# Solution: Change port in .env
FLASK_PORT=5002
```

#### 2. Database Connection Error
```bash
# Error: could not connect to server
# Solution: Check database URL and credentials
DATABASE_URL="postgresql://user:pass@host:5432/db"
```

#### 3. OCR Not Working
```bash
# Error: poppler not found
# Solution: Install poppler and update path
POPPLER_PATH="C:\\poppler\\poppler-24.08.0\\Library\\bin"
```

#### 4. File Upload Issues
```bash
# Error: File too large
# Solution: Check file size limits in config.py
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### Debug Mode

Enable debug mode untuk development:

```bash
# Set environment variable
export FLASK_DEBUG=1

# Or in .env file
FLASK_DEBUG=1
```

## 🔒 Security

### Environment Variables

- Jangan commit file `.env` ke repository
- Gunakan service role key untuk Supabase
- Validasi semua input dari user
- Implement rate limiting untuk API

### File Upload Security

- Validate file types
- Scan uploaded files
- Limit file size
- Store files securely

## 📦 Deployment

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set DATABASE_URL=your-database-url
heroku config:set POPPLER_PATH=/app/.apt/usr/bin

# Deploy
git push heroku main
```

### Docker Deployment

```bash
# Build image
docker build -t proyek-pajak-backend .

# Run container
docker run -p 5001:5001 --env-file .env proyek-pajak-backend
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Taufiqu**
- GitHub: [@Taufiqu](https://github.com/Taufiqu)

## 🙏 Acknowledgments

- EasyOCR untuk OCR processing
- Supabase untuk database hosting
- Flask framework
- All contributors dan libraries yang digunakan

## 📞 Support

Jika ada pertanyaan atau issue:
1. Buka issue di GitHub repository
2. Check troubleshooting section
3. Review dokumentasi API

---

**⚡ Happy Coding!**
