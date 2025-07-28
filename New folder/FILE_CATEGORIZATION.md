# 📁 FILE CATEGORIZATION FOR DIRECTORY SEPARATION

## 🗂️ CURRENT STRUCTURE ANALYSIS

Berikut adalah kategorisasi lengkap semua file untuk membantu pemisahan directory:

---

## 🏢 **SHARED/COMMON FILES** (Digunakan oleh kedua service)
```
📁 shared_files/
├── 🐍 models.py                    # Database models (PPNMasukan, PPNKeluaran, BuktiSetor)
├── ⚙️ config.py                   # Configuration untuk kedua service
├── 📁 migrations/                 # Database migrations
├── 📁 shared_utils/               # Utilities bersama
│   ├── file_utils.py              # File handling utilities
│   ├── image_utils.py             # Image processing utilities
│   └── text_utils.py              # Text processing utilities
├── 📁 templates/                  # Excel templates
├── 🗄️ SUPABASE_SETUP.md          # Database setup guide
└── 🐍 app.py                      # Main app (untuk development)
```

---

## 📄 **FAKTUR SERVICE FILES** (Tesseract OCR)
```
📁 faktur_service/
├── 🐍 app_faktur.py               # Main application file
├── 🐳 Dockerfile.faktur           # Docker container config
├── 📦 requirements-faktur.txt     # Python dependencies
├── 🚂 railway-faktur.toml         # Railway deployment config
├── 📝 Procfile.faktur             # Process file for deployment
└── 📁 faktur/                     # Faktur module
    ├── 📁 services/               # Business logic
    │   ├── __init__.py
    │   ├── delete.py              # Delete operations
    │   ├── excel_exporter.py      # Excel export functionality
    │   ├── file_saver.py          # File saving operations
    │   ├── history.py             # History operations
    │   └── invoice_processor.py   # Main OCR processing (Tesseract)
    └── 📁 utils/                  # Faktur utilities
        ├── __init__.py
        ├── helpers.py             # Helper functions
        ├── preprocessing.py       # Image preprocessing for Tesseract
        └── 📁 extraction/         # Data extraction utilities
```

---

## 🧾 **BUKTI SETOR SERVICE FILES** (EasyOCR)
```
📁 bukti_setor_service/
├── 🐍 app_bukti_setor.py          # Main application file
├── 🐳 Dockerfile.bukti-setor      # Docker container config
├── 📦 requirements-bukti-setor.txt # Python dependencies
├── 🚂 railway-bukti-setor.toml    # Railway deployment config
├── 📝 Procfile.bukti-setor        # Process file for deployment
└── 📁 bukti_setor/                # Bukti setor module
    ├── __init__.py
    ├── routes.py                  # Flask routes/blueprints
    ├── 📁 services/               # Business logic
    │   ├── delete.py              # Delete operations
    │   └── excel_exporter_bukti_setor.py # Excel export
    └── 📁 utils/                  # Bukti setor utilities
        ├── __init__.py
        ├── bukti_setor_processor.py # Main OCR processing (EasyOCR)
        ├── ocr_engine.py          # EasyOCR engine wrapper
        ├── spellcheck.py          # Spell checking utilities
        ├── helpers.py             # Helper functions
        ├── kamus_indonesia.txt    # Indonesian dictionary
        └── 📁 parsing/            # Data parsing utilities
            ├── tanggal.py         # Date parsing
            ├── jumlah.py          # Amount parsing
            └── kode_setor.py      # Deposit code parsing
```

---

## 🔧 **DEVELOPMENT & DEPLOYMENT FILES**
```
📁 deployment_config/
├── 🐳 docker-compose.dev.yml      # Development environment
├── 🔧 dev-setup.sh               # Development setup (Linux/Mac)
├── 🔧 dev-setup.bat              # Development setup (Windows)
├── 🚂 deploy-railway.ps1         # Deployment script (PowerShell)
├── 🚂 deploy-railway.sh          # Deployment script (Bash)
├── 🔒 .env.example               # Environment template
├── 🚫 .dockerignore              # Docker ignore rules
├── 🚫 .gitignore                 # Git ignore rules
└── 📦 requirements.txt           # Base requirements (legacy)
```

---

## 📚 **DOCUMENTATION FILES**
```
📁 documentation/
├── 📖 README.md                   # Main documentation
├── 📖 RAILWAY_DEPLOYMENT.md       # Railway deployment guide
├── 📖 API_DOCS_SEPARATED.md       # API documentation
├── 📖 DEPLOYMENT_SUMMARY.md       # Deployment summary
├── 📖 DEPLOYMENT_ARCHITECTURE.md  # Architecture overview
├── 📖 CHANGELOG.md               # Change log
├── 📖 CONTRIBUTING.md            # Contributing guidelines
└── 📜 LICENSE                    # License file
```

---

## 🧪 **SYSTEM/MISC FILES**
```
📁 system/
└── 📦 Aptfile                    # System packages (untuk Railway)
```

---

## 🎯 **PROPOSED NEW DIRECTORY STRUCTURE**

```
📁 ocr-tax-processing/
├── 📁 faktur-service/            # Faktur OCR Service
│   ├── app_faktur.py
│   ├── Dockerfile.faktur
│   ├── requirements-faktur.txt
│   ├── railway-faktur.toml
│   ├── Procfile.faktur
│   └── faktur/
├── 📁 bukti-setor-service/       # Bukti Setor OCR Service
│   ├── app_bukti_setor.py
│   ├── Dockerfile.bukti-setor
│   ├── requirements-bukti-setor.txt
│   ├── railway-bukti-setor.toml
│   ├── Procfile.bukti-setor
│   └── bukti_setor/
├── 📁 shared/                    # Shared components
│   ├── models.py
│   ├── config.py
│   ├── migrations/
│   ├── shared_utils/
│   └── templates/
├── 📁 deployment/                # Deployment configs
│   ├── docker-compose.dev.yml
│   ├── dev-setup.*
│   ├── .env.example
│   └── deploy-scripts/
├── 📁 docs/                      # Documentation
│   ├── README.md
│   ├── API_DOCS_SEPARATED.md
│   └── guides/
└── 📁 system/                    # System files
    ├── .gitignore
    ├── .dockerignore
    └── Aptfile
```

---

## 🚀 **MIGRATION STRATEGY**

### Phase 1: Create Directory Structure
1. Create new directories
2. Move shared components first
3. Move service-specific files

### Phase 2: Update Import Paths
1. Update relative imports in Python files
2. Update Docker paths
3. Update configuration references

### Phase 3: Update Deployment Configs
1. Update Dockerfile paths
2. Update Railway configurations
3. Update documentation

Apakah Anda ingin saya membantu membuat script untuk melakukan migration ini secara otomatis?
