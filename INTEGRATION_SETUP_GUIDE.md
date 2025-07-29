# 🔧 INTEGRATION SETUP GUIDE
**Panduan Lengkap Integrasi Database & File Management**

---

## 📊 DATABASE CONFIGURATION

### **Environment Variables untuk Railway Services**

Copy environment variables ini ke **Railway Dashboard** untuk kedua services:

```env
# Database Connection
DATABASE_URL=postgresql://postgres.hodllrhwyqhrksfkgiqc:26122004dbpajak@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres

# Supabase Configuration
SUPABASE_URL=https://hodllrhwyqhrksfkgiqc.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvZGxscmh3eXFocmtzZmtnaXFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjY3NjQyMCwiZXhwIjoyMDUyMjUyNDIwfQ.lAOT5VnU8Kev-aOSDnpG6_Sojsg_SU8-TS1y0YE57Zw

# Application Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 🗄️ DATABASE MODELS

### **1. Model untuk Faktur Service**

```python
# models.py untuk Faktur Service
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PPNMasukan(db.Model):
    __tablename__ = 'ppn_masukan'
    
    id = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(20), nullable=False)  # 'masukan' atau 'keluaran'
    no_faktur = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    nama_lawan_transaksi = db.Column(db.String(200), nullable=False)
    dpp = db.Column(db.Numeric(15, 2), nullable=False)
    ppn = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'jenis': self.jenis,
            'no_faktur': self.no_faktur,
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'nama_lawan_transaksi': self.nama_lawan_transaksi,
            'dpp': float(self.dpp),
            'ppn': float(self.ppn),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
```

### **2. Model untuk Bukti Setor Service**

```python
# models.py untuk Bukti Setor Service
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BuktiSetor(db.Model):
    __tablename__ = 'bukti_setor'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_setor = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jumlah = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_setor': self.kode_setor,
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'jumlah': float(self.jumlah),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
```

---

## 🔧 DATABASE ENDPOINTS

### **Faktur Service - Tambah Endpoints Ini**

```python
# app.py untuk Faktur Service
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, PPNMasukan

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# CRUD Endpoints
@app.route('/api/save-faktur', methods=['POST'])
def save_faktur():
    """Save processed faktur data to database"""
    try:
        data = request.get_json()
        
        # Support bulk save
        if isinstance(data, list):
            saved_count = 0
            for item in data:
                if all(key in item for key in ['jenis', 'no_faktur', 'tanggal', 'nama_lawan_transaksi', 'dpp', 'ppn']):
                    tanggal_obj = datetime.strptime(item['tanggal'], '%Y-%m-%d').date()
                    
                    new_record = PPNMasukan(
                        jenis=item['jenis'],
                        no_faktur=item['no_faktur'],
                        tanggal=tanggal_obj,
                        nama_lawan_transaksi=item['nama_lawan_transaksi'],
                        dpp=float(item['dpp']),
                        ppn=float(item['ppn'])
                    )
                    db.session.add(new_record)
                    saved_count += 1
            
            db.session.commit()
            return jsonify(message=f"{saved_count} faktur berhasil disimpan!"), 201
        
        # Single record save
        else:
            if not all(key in data for key in ['jenis', 'no_faktur', 'tanggal', 'nama_lawan_transaksi', 'dpp', 'ppn']):
                return jsonify(error="Field tidak lengkap"), 400
            
            tanggal_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
            
            new_record = PPNMasukan(
                jenis=data['jenis'],
                no_faktur=data['no_faktur'],
                tanggal=tanggal_obj,
                nama_lawan_transaksi=data['nama_lawan_transaksi'],
                dpp=float(data['dpp']),
                ppn=float(data['ppn'])
            )
            
            db.session.add(new_record)
            db.session.commit()
            return jsonify(message="Faktur berhasil disimpan!"), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Error saving faktur: {str(e)}"), 500

@app.route('/api/faktur-history', methods=['GET'])
def get_faktur_history():
    """Get all faktur records"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        results = db.session.execute(
            db.select(PPNMasukan)
            .order_by(PPNMasukan.tanggal.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).scalars().all()
        
        data = [record.to_dict() for record in results]
        return jsonify(message="Data berhasil diambil.", data=data), 200
        
    except Exception as e:
        return jsonify(error=f"Error fetching data: {str(e)}"), 500

@app.route('/api/faktur/<int:id>', methods=['DELETE'])
def delete_faktur(id):
    """Delete faktur record by ID"""
    try:
        record = db.session.get(PPNMasukan, id)
        if not record:
            return jsonify(error="Data tidak ditemukan"), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify(message="Data berhasil dihapus"), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Error deleting data: {str(e)}"), 500
```

### **Bukti Setor Service - Tambah Endpoints Ini**

```python
# app.py untuk Bukti Setor Service
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, BuktiSetor

# Database configuration (sama seperti di atas)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# CRUD Endpoints
@app.route('/api/save-bukti-setor', methods=['POST'])
def save_bukti_setor():
    """Save processed bukti setor data to database"""
    try:
        data = request.get_json()
        
        # Support bulk save
        if isinstance(data, list):
            saved_count = 0
            for item in data:
                if all(key in item for key in ['kode_setor', 'tanggal', 'jumlah']):
                    tanggal_obj = datetime.strptime(item['tanggal'], '%Y-%m-%d').date()
                    
                    new_record = BuktiSetor(
                        kode_setor=item['kode_setor'],
                        tanggal=tanggal_obj,
                        jumlah=float(item['jumlah'])
                    )
                    db.session.add(new_record)
                    saved_count += 1
            
            db.session.commit()
            return jsonify(message=f"{saved_count} bukti setor berhasil disimpan!"), 201
        
        # Single record save
        else:
            if not all(key in data for key in ['kode_setor', 'tanggal', 'jumlah']):
                return jsonify(error="Field tidak lengkap"), 400
            
            tanggal_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()
            
            new_record = BuktiSetor(
                kode_setor=data['kode_setor'],
                tanggal=tanggal_obj,
                jumlah=float(data['jumlah'])
            )
            
            db.session.add(new_record)
            db.session.commit()
            return jsonify(message="Bukti setor berhasil disimpan!"), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Error saving bukti setor: {str(e)}"), 500

@app.route('/api/bukti-setor-history', methods=['GET'])
def get_bukti_setor_history():
    """Get all bukti setor records"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        results = db.session.execute(
            db.select(BuktiSetor)
            .order_by(BuktiSetor.tanggal.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).scalars().all()
        
        data = [record.to_dict() for record in results]
        return jsonify(message="Data berhasil diambil.", data=data), 200
        
    except Exception as e:
        return jsonify(error=f"Error fetching data: {str(e)}"), 500

@app.route('/api/bukti-setor/<int:id>', methods=['DELETE'])
def delete_bukti_setor(id):
    """Delete bukti setor record by ID"""
    try:
        record = db.session.get(BuktiSetor, id)
        if not record:
            return jsonify(error="Data tidak ditemukan"), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify(message="Data berhasil dihapus"), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Error deleting data: {str(e)}"), 500
```

---

## 📁 FILE MANAGEMENT DENGAN SUPABASE STORAGE

### **1. Setup Supabase Storage**

**Di Supabase Dashboard:**
1. Go to **Storage** > **Buckets**
2. Create new bucket: `uploads`
3. Set bucket sebagai **Public**
4. Get Storage URL: `https://hodllrhwyqhrksfkgiqc.supabase.co/storage/v1/object/public/uploads/`

### **2. Install Dependencies**

```bash
# Tambah ke requirements.txt di kedua services
supabase==2.3.4
```

### **3. File Upload Utility**

```python
# utils/supabase_storage.py
import os
from supabase import create_client
import hashlib
import time

class SupabaseStorage:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        )
        self.bucket_name = 'uploads'
    
    def upload_file(self, file_data, original_filename, folder='preview'):
        """Upload file to Supabase Storage"""
        try:
            # Generate unique filename
            timestamp = str(int(time.time()))
            file_hash = hashlib.md5(file_data).hexdigest()[:8]
            filename = f"{folder}/{timestamp}_{file_hash}_{original_filename}"
            
            # Upload to Supabase
            result = self.supabase.storage.from_(self.bucket_name).upload(
                filename, file_data
            )
            
            if result.status_code in [200, 201]:
                # Return public URL
                return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{self.bucket_name}/{filename}"
            else:
                print(f"Upload failed: {result}")
                return None
                
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None
    
    def delete_file(self, filename):
        """Delete file from Supabase Storage"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).remove([filename])
            return result.status_code == 200
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False

# Usage in your services
storage = SupabaseStorage()

# Upload preview image
def save_preview_to_cloud(image_data, filename):
    public_url = storage.upload_file(image_data, filename, 'preview')
    return public_url

# Delete file
def delete_preview_from_cloud(filename):
    return storage.delete_file(filename)
```

### **4. Update Preview Image Handling**

```python
# Di kedua services, update fungsi save preview
def simpan_preview_image(pil_image, upload_folder, page_num=1, original_filename="document"):
    """Save preview image to Supabase Storage instead of local"""
    try:
        # Convert PIL image to bytes
        import io
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Generate filename
        base_filename = os.path.splitext(original_filename)[0]
        preview_filename = f"{base_filename}_hal_{page_num}.jpg"
        
        # Upload to Supabase
        storage = SupabaseStorage()
        public_url = storage.upload_file(img_byte_arr, preview_filename, 'preview')
        
        if public_url:
            return preview_filename, public_url
        else:
            raise Exception("Failed to upload to Supabase Storage")
            
    except Exception as e:
        print(f"Error saving preview: {str(e)}")
        return None, None
```

---

## 🔄 UPDATE REQUIREMENTS.TXT

```txt
# Tambah dependencies ini ke kedua services
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
psycopg2-binary==2.9.7
supabase==2.3.4
python-dotenv==1.0.0
```

---

## 🚀 DEPLOYMENT CHECKLIST

### **Railway Environment Variables Setup**

**Untuk Faktur Service:**
- [x] DATABASE_URL
- [x] SUPABASE_URL  
- [x] SUPABASE_SERVICE_ROLE_KEY
- [x] FLASK_ENV=production

**Untuk Bukti Setor Service:**
- [x] DATABASE_URL
- [x] SUPABASE_URL
- [x] SUPABASE_SERVICE_ROLE_KEY  
- [x] FLASK_ENV=production

### **Testing Endpoints**

**Test Database Connection:**
```bash
# Test faktur service
curl https://your-faktur-service.up.railway.app/api/faktur-history

# Test bukti setor service  
curl https://your-bukti-setor-service.up.railway.app/api/bukti-setor-history
```

**Test Save Functionality:**
```bash
# Test save faktur
curl -X POST https://your-faktur-service.up.railway.app/api/save-faktur \
  -H "Content-Type: application/json" \
  -d '{"jenis":"masukan","no_faktur":"123","tanggal":"2024-01-15","nama_lawan_transaksi":"Test","dpp":100000,"ppn":10000}'

# Test save bukti setor
curl -X POST https://your-bukti-setor-service.up.railway.app/api/save-bukti-setor \
  -H "Content-Type: application/json" \
  -d '{"kode_setor":"411211","tanggal":"2024-01-15","jumlah":"100000"}'
```

---

## 📱 FRONTEND UPDATE

### **Update API URLs di Frontend**

```javascript
// config/api.js
const API_CONFIG = {
  FAKTUR_SERVICE: "https://your-faktur-service.up.railway.app",
  BUKTI_SETOR_SERVICE: "https://your-bukti-setor-service.up.railway.app"
};

// Update all API calls
const processFaktur = (file) => {
  return axios.post(`${API_CONFIG.FAKTUR_SERVICE}/process`, formData);
};

const saveFaktur = (data) => {
  return axios.post(`${API_CONFIG.FAKTUR_SERVICE}/api/save-faktur`, data);
};

const getFakturHistory = () => {
  return axios.get(`${API_CONFIG.FAKTUR_SERVICE}/api/faktur-history`);
};

// Similar untuk bukti setor...
```

---

## ⚠️ IMPORTANT NOTES

1. **Database Tables**: Tables akan otomatis dibuat saat first deployment dengan `db.create_all()`

2. **File URLs**: Setelah migrasi ke Supabase Storage, semua preview URLs akan berformat:
   `https://hodllrhwyqhrksfkgiqc.supabase.co/storage/v1/object/public/uploads/preview/filename.jpg`

3. **CORS**: Pastikan CORS dikonfigurasi untuk allow frontend domain

4. **Error Handling**: Semua endpoints sudah include proper error handling dan logging

5. **Pagination**: History endpoints support pagination dengan query params `page` dan `per_page`

---

**File ini berisi semua informasi yang dibutuhkan untuk setup database dan file management di repo deployment. Copy semua kode dan konfigurasi ini ke chat repo deployment untuk implementasi.** 🚀
