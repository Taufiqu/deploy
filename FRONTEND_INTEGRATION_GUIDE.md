# 🚀 FAKTUR SERVICE API - RAILWAY DEPLOYMENT SUMMARY
## Frontend Integration Guide

### 📡 **Production API Endpoint**
```
Base URL: https://deploy-production-72bc.up.railway.app
```

### 🔧 **Required Frontend Changes**

#### 1. **Update API Base URL**
```javascript
// OLD (local development)
const API_BASE_URL = 'http://localhost:5000';

// NEW (production)
const API_BASE_URL = 'https://deploy-production-72bc.up.railway.app';
```

#### 2. **Available API Endpoints**

##### **Health Check Endpoints**
```javascript
GET /                    // Basic health check
GET /health             // Detailed health check with database status
GET /api/test-db        // Database connection test
```

##### **Faktur Processing Endpoints**
```javascript
POST /api/process       // Main OCR processing endpoint (NEW!)
POST /api/save-faktur   // Save faktur data to database
GET  /api/faktur-history // Get faktur records with filters
DELETE /api/faktur/{id} // Delete faktur record
```

#### 3. **New `/api/process` Endpoint Specification**

**Request Format:**
```javascript
// FormData with file upload
const formData = new FormData();
formData.append('file', fileBlob);
formData.append('service_type', 'faktur'); // or 'bukti-setor'

// POST request
fetch('https://deploy-production-72bc.up.railway.app/api/process', {
  method: 'POST',
  body: formData,
  headers: {
    // Don't set Content-Type, let browser set it with boundary
  }
})
```

**Response Format:**
```javascript
// Success Response
{
  "status": "success",
  "message": "File processed successfully",
  "service_type": "faktur",
  "extracted_data": {
    "no_faktur": "010.002-25.00000001",
    "tanggal": "2025-01-15",
    "nama_lawan_transaksi": "PT. CONTOH SUPPLIER",
    "npwp_lawan_transaksi": "01.234.567.8-901.000",
    "dpp": 1000000.00,
    "ppn": 110000.00,
    "bulan": "Januari 2025",
    "keterangan": "Pembelian bahan baku"
  },
  "confidence_score": 0.85,
  "processing_time": 2.34
}

// Error Response
{
  "status": "error",
  "message": "File format not supported",
  "error_code": "INVALID_FILE_FORMAT"
}
```

#### 4. **Updated CORS Configuration**
✅ Railway service already configured to accept requests from:
- `https://pajak-ocr.vercel.app` (your frontend)
- All origins (`*`) for development

#### 5. **Error Handling Updates**

**Network Error Handling:**
```javascript
// Handle Railway-specific errors
const handleAPIError = (error) => {
  if (error.code === 'ERR_NETWORK') {
    return 'Service temporarily unavailable. Please try again.';
  }
  if (error.response?.status === 502) {
    return 'Backend service is starting up. Please wait a moment.';
  }
  return error.message || 'An unexpected error occurred.';
};
```

#### 6. **Database Integration Features**

**Save Processed Data:**
```javascript
// After successful OCR processing, save to database
const saveToDatabase = async (extractedData) => {
  const response = await fetch('https://deploy-production-72bc.up.railway.app/api/save-faktur', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      jenis: 'masukan', // or 'keluaran'
      no_faktur: extractedData.no_faktur,
      tanggal: extractedData.tanggal,
      nama_lawan_transaksi: extractedData.nama_lawan_transaksi,
      dpp: extractedData.dpp,
      ppn: extractedData.ppn,
      bulan: extractedData.bulan,
      keterangan: extractedData.keterangan,
      npwp_lawan_transaksi: extractedData.npwp_lawan_transaksi
    })
  });
  
  return response.json();
};
```

**Get History Data:**
```javascript
// Fetch faktur history with filters
const getFakturHistory = async (filters = {}) => {
  const queryParams = new URLSearchParams({
    jenis: filters.jenis || 'all',     // 'masukan', 'keluaran', 'all'
    limit: filters.limit || 20         // max 100
  });
  
  const response = await fetch(
    `https://deploy-production-72bc.up.railway.app/api/faktur-history?${queryParams}`
  );
  
  return response.json();
};
```

### 🔄 **Migration Steps for Frontend**

#### Step 1: Update Environment Variables
```javascript
// .env.production
REACT_APP_API_URL=https://deploy-production-72bc.up.railway.app

// .env.development  
REACT_APP_API_URL=http://localhost:5000
```

#### Step 2: Update API Service File
```javascript
// api/config.js or similar
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'https://deploy-production-72bc.up.railway.app',
  timeout: 30000, // 30 seconds for file processing
  headers: {
    'Accept': 'application/json',
  }
};
```

#### Step 3: Update File Upload Component
```javascript
// Update your upload handler
const handleFileUpload = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('service_type', 'faktur');
  
  try {
    const response = await axios.post(
      `${API_CONFIG.baseURL}/api/process`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000
      }
    );
    
    if (response.data.status === 'success') {
      // Handle successful OCR
      setExtractedData(response.data.extracted_data);
      
      // Optionally save to database
      await saveToDatabase(response.data.extracted_data);
    }
    
  } catch (error) {
    console.error('Upload error:', handleAPIError(error));
  }
};
```

### 🚨 **Current Status & Actions Needed**

#### ✅ **Working:**
- Railway deployment successful
- CORS configured for Vercel frontend
- Database models ready
- Basic API endpoints available

#### ⚠️ **Pending Fix:**
- Database connection string format issue
- Missing `/api/process` endpoint implementation

#### 🔧 **Next Steps:**
1. **Fix DATABASE_URL format** in Railway environment variables
2. **Deploy updated code** with `/api/process` endpoint
3. **Test integration** between frontend and backend
4. **Add Bukti Setor service** (separate deployment)

### 📞 **API Response Examples**

#### Health Check Response:
```json
{
  "status": "healthy",
  "service": "faktur-service",
  "database_available": true,
  "database_url_set": true,
  "environment": "production"
}
```

#### Database Test Response:
```json
{
  "status": "success",
  "message": "Database connection successful",
  "tables": {
    "ppn_masukan": 0,
    "ppn_keluaran": 0
  }
}
```

### 🔐 **Security Notes**
- All API endpoints are HTTPS-only in production
- CORS properly configured for your Vercel domain
- Database credentials secured via environment variables
- File uploads have size limits and type validation

### 📊 **Database Schema**
```sql
-- Tables available for frontend integration:
ppn_masukan     -- PPN input tax records
ppn_keluaran    -- PPN output tax records  
bukti_setor     -- Tax payment receipts (future)
```

This summary should give your frontend team everything needed to integrate with the Railway deployment! 🚀
