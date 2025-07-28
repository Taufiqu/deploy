# 📡 API Documentation - Separated Services

This document describes the API endpoints for the separated OCR services.

## 🏗️ Architecture Overview

The application is split into two independent services:

- **Faktur Service** (Port 5001) - Tesseract OCR for invoice processing
- **Bukti Setor Service** (Port 5002) - EasyOCR for payment receipt processing

Both services share the same PostgreSQL database but run independently.

---

## 🧾 Faktur Service API (Tesseract OCR)

**Base URL**: `http://localhost:5001` (development) or `https://your-faktur-domain.railway.app` (production)

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "faktur-ocr",
  "ocr_engine": "tesseract",
  "version": "1.0.0"
}
```

### Upload and Process Invoice
```http
POST /api/faktur/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: PDF or image file (required)
- `jenis_pajak`: "masukan" or "keluaran" (optional, default: "masukan")

**Response:**
```json
{
  "message": "Faktur processed successfully",
  "data": {
    "no_faktur": "010.000-24.00000001",
    "tanggal": "2024-01-15",
    "npwp_lawan_transaksi": "12.345.678.9-012.000",
    "nama_lawan_transaksi": "PT CONTOH PERUSAHAAN",
    "dpp": 1000000.00,
    "ppn": 110000.00,
    "keterangan": "Pembelian barang",
    "preview_filename": "preview_faktur_001.jpg"
  },
  "saved": true,
  "ocr_engine": "tesseract"
}
```

### Get Invoice History
```http
GET /api/faktur/history/{jenis_pajak}
```

**Parameters:**
- `jenis_pajak`: "masukan" or "keluaran"

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "no_faktur": "010.000-24.00000001",
      "tanggal": "2024-01-15",
      "npwp_lawan_transaksi": "12.345.678.9-012.000",
      "nama_lawan_transaksi": "PT CONTOH PERUSAHAAN",
      "dpp": 1000000.00,
      "ppn": 110000.00,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### Export to Excel
```http
GET /api/faktur/export/{jenis_pajak}
```

**Parameters:**
- `jenis_pajak`: "masukan" or "keluaran"

**Response:**
```json
{
  "message": "Excel generated successfully",
  "file_path": "/path/to/export.xlsx"
}
```

### Delete Invoice
```http
DELETE /api/faktur/delete/{faktur_id}?jenis_pajak={jenis_pajak}
```

**Parameters:**
- `faktur_id`: Invoice ID (in URL)
- `jenis_pajak`: "masukan" or "keluaran" (query parameter)

**Response:**
```json
{
  "message": "Invoice deleted successfully",
  "deleted_id": 1
}
```

---

## 🧾 Bukti Setor Service API (EasyOCR)

**Base URL**: `http://localhost:5002` (development) or `https://your-bukti-setor-domain.railway.app` (production)

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "bukti-setor-ocr",
  "ocr_engine": "easyocr",
  "version": "1.0.0"
}
```

### Service Information
```http
GET /api/info
```

**Response:**
```json
{
  "service": "Bukti Setor OCR Service",
  "ocr_engine": "EasyOCR",
  "supported_languages": ["id", "en"],
  "supported_formats": ["PDF", "JPG", "PNG", "JPEG"],
  "features": [
    "OCR processing with EasyOCR",
    "Spell checking",
    "Data validation",
    "Excel export",
    "History tracking"
  ]
}
```

### Upload and Process Receipt
```http
POST /api/bukti-setor/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: PDF or image file (required)

**Response:**
```json
{
  "message": "Bukti setor processed successfully",
  "data": {
    "tanggal": "2024-01-15",
    "kode_setor": "411128",
    "jumlah": 500000.00,
    "preview_filename": "preview_bukti_setor_001.jpg"
  },
  "saved": true,
  "ocr_engine": "easyocr"
}
```

### Get Receipt History
```http
GET /api/bukti-setor/history
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "tanggal": "2024-01-15",
      "kode_setor": "411128",
      "jumlah": 500000.00,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### Export to Excel
```http
GET /api/laporan/export
```

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD, optional)
- `end_date`: End date (YYYY-MM-DD, optional)

**Response:**
```json
{
  "message": "Excel generated successfully",
  "file_path": "/path/to/export.xlsx"
}
```

### Delete Receipt
```http
DELETE /api/bukti-setor/delete/{receipt_id}
```

**Parameters:**
- `receipt_id`: Receipt ID (in URL)

**Response:**
```json
{
  "message": "Receipt deleted successfully",
  "deleted_id": 1
}
```

---

## 🔧 Error Responses

All services return consistent error responses:

### 400 Bad Request
```json
{
  "error": "No file provided"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

### 413 Payload Too Large
```json
{
  "error": "File too large. Maximum size is 16MB"
}
```

### 500 Internal Server Error
```json
{
  "error": "Processing failed: [error details]"
}
```

---

## 🔄 Cross-Service Communication

Both services are independent but share the same database. They don't communicate directly with each other. If you need to aggregate data from both services, your frontend/client should make separate requests to each service.

### Example: Get All Data
```javascript
// Get invoice data
const faktureData = await fetch('http://faktur-service/api/faktur/history/masukan');

// Get receipt data  
const buktiSetorData = await fetch('http://bukti-setor-service/api/bukti-setor/history');

// Combine data on client side
const combinedData = {
  faktur: await faktureData.json(),
  bukti_setor: await buktiSetorData.json()
};
```

---

## 🚀 Deployment URLs

### Railway Deployment
- **Faktur Service**: `https://faktur-ocr-service-production.up.railway.app`
- **Bukti Setor Service**: `https://bukti-setor-ocr-service-production.up.railway.app`

### Development
- **Faktur Service**: `http://localhost:5001`
- **Bukti Setor Service**: `http://localhost:5002`

---

## 📝 Usage Examples

### cURL Examples

**Upload Invoice:**
```bash
curl -X POST \
  http://localhost:5001/api/faktur/upload \
  -F "file=@invoice.pdf" \
  -F "jenis_pajak=masukan"
```

**Upload Receipt:**
```bash
curl -X POST \
  http://localhost:5002/api/bukti-setor/upload \
  -F "file=@receipt.pdf"
```

### JavaScript/Fetch Examples

**Upload Invoice:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('jenis_pajak', 'masukan');

const response = await fetch('http://localhost:5001/api/faktur/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

**Upload Receipt:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5002/api/bukti-setor/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```
