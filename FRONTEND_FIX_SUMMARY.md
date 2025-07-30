# 🔧 FRONTEND FIX - RAILWAY INTEGRATION
## Summary untuk Chat Frontend

### 🚨 **Masalah yang Harus Diperbaiki:**

Dari console log terlihat:
```
🧠 currentPage (dari formPages): undefined
🖼️ preview_image: undefined  
🔍 src: undefined/preview/undefined
```

**Root Cause:** Response structure dari Railway backend berbeda dengan local backend.

### 📊 **Response Structure Baru dari Railway:**

#### **SUCCESS Response:**
```json
{
  "status": "success",
  "message": "File processed successfully",
  "service_type": "faktur",
  "extracted_data": {
    "no_faktur": "010.002-25.12345678",
    "tanggal": "2025-01-15",
    "nama_lawan_transaksi": "PT. MULTI INTAN PERKASA",
    "npwp_lawan_transaksi": "12.345.678.9-012.345",
    "dpp": 1500000.00,
    "ppn": 165000.00,
    "bulan": "Januari 2025",
    "keterangan": "Faktur dari file: done (1).jpg"
  },
  "confidence_score": 0.89,
  "processing_time": 1.23,
  "filename": "done (1).jpg",
  "mode": "demo"
}
```

#### **ERROR Response:**
```json
{
  "status": "error",
  "message": "Error description",
  "error_code": "ERROR_TYPE"
}
```

### 🔄 **Frontend Changes Required:**

#### **1. Update Response Handler (MainOCRPage.jsx):**

**OLD CODE (yang error):**
```javascript
// Assuming old structure
const handleUpload = async (file) => {
  // ... upload logic
  
  // OLD - probably looking for different structure
  if (response.data.currentPage) {
    setCurrentPage(response.data.currentPage);
  }
  if (response.data.preview_image) {
    setPreviewImage(response.data.preview_image);
  }
}
```

**NEW CODE (fix):**
```javascript
const handleUpload = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('service_type', 'faktur');
    
    const response = await axios.post(
      `${API_CONFIG.baseURL}/api/process`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000
      }
    );
    
    // Handle Railway response structure
    if (response.data.status === 'success') {
      const { extracted_data, filename, mode } = response.data;
      
      // Set extracted data to state
      setExtractedData(extracted_data);
      
      // Handle filename and preview
      setCurrentFileName(filename);
      
      // Generate preview path (adjust based on your preview logic)
      const previewPath = `/preview/${filename}`;
      setPreviewImage(previewPath);
      
      // Set current page (if you have pagination logic)
      setCurrentPage(1); // or based on your logic
      
      // Show success message
      showNotification(`File ${filename} processed successfully!`, 'success');
      
      // Log for debugging
      console.log('✅ Railway Processing Success:', {
        filename,
        mode,
        extractedData: extracted_data
      });
      
    } else {
      // Handle error response
      throw new Error(response.data.message || 'Processing failed');
    }
    
  } catch (error) {
    console.error('❌ Upload error:', error);
    
    // Handle specific error types
    if (error.response?.data?.error_code) {
      switch (error.response.data.error_code) {
        case 'NO_FILE':
          showNotification('Please select a file to upload', 'error');
          break;
        case 'INVALID_FILE_TYPE':
          showNotification('File type not supported. Please upload PNG, JPG, JPEG, or PDF files.', 'error');
          break;
        case 'DB_UNAVAILABLE':
          showNotification('Database service temporarily unavailable. Please try again.', 'error');
          break;
        default:
          showNotification(error.response.data.message || 'Processing failed', 'error');
      }
    } else {
      showNotification('Network error. Please check your connection.', 'error');
    }
  }
};
```

#### **2. Update State Management:**

```javascript
// Add new state variables if needed
const [currentFileName, setCurrentFileName] = useState('');
const [processingMode, setProcessingMode] = useState('');
const [confidenceScore, setConfidenceScore] = useState(0);

// Update existing state setters
const [extractedData, setExtractedData] = useState({
  no_faktur: '',
  tanggal: '',
  nama_lawan_transaksi: '',
  npwp_lawan_transaksi: '',
  dpp: 0,
  ppn: 0,
  bulan: '',
  keterangan: ''
});
```

#### **3. Update Form Fields Mapping:**

```javascript
// Map extracted_data to form fields
const updateFormFromExtractedData = (data) => {
  // Update form fields based on extracted_data structure
  setFormData({
    ...formData,
    noFaktur: data.no_faktur || '',
    tanggal: data.tanggal || '',
    namaLawanTransaksi: data.nama_lawan_transaksi || '',
    npwpLawanTransaksi: data.npwp_lawan_transaksi || '',
    dpp: data.dpp || 0,
    ppn: data.ppn || 0,
    bulan: data.bulan || '',
    keterangan: data.keterangan || ''
  });
};

// Call this after successful response
updateFormFromExtractedData(response.data.extracted_data);
```

#### **4. Fix Preview Image Logic:**

```javascript
// Update preview image handling
const handlePreviewImage = (filename) => {
  // Option 1: If you have a preview endpoint
  const previewUrl = `${API_CONFIG.baseURL}/api/preview/${filename}`;
  setPreviewImage(previewUrl);
  
  // Option 2: If you generate preview client-side
  // Keep your existing logic but ensure filename is available
  
  // Option 3: Use original file as preview
  if (file) {
    const objectUrl = URL.createObjectURL(file);
    setPreviewImage(objectUrl);
  }
};
```

#### **5. Add Debug Logging:**

```javascript
// Add comprehensive logging for debugging
const debugLog = (stage, data) => {
  console.log(`🔍 ${stage}:`, data);
};

// Use in your upload handler
debugLog('Upload Start', { file: file.name, size: file.size });
debugLog('API Response', response.data);
debugLog('Extracted Data', response.data.extracted_data);
debugLog('Form Update', formData);
```

#### **6. Update Error Handling:**

```javascript
// Enhanced error handling
const handleAPIError = (error) => {
  console.error('API Error Details:', {
    status: error.response?.status,
    data: error.response?.data,
    message: error.message
  });
  
  // Return user-friendly message
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  
  switch (error.response?.status) {
    case 400:
      return 'Invalid request. Please check your file and try again.';
    case 503:
      return 'Service temporarily unavailable. Please try again in a moment.';
    case 500:
      return 'Server error. Please try again later.';
    default:
      return 'Network error. Please check your connection.';
  }
};
```

### 🧪 **Testing Checklist:**

After implementing these changes, test:

1. ✅ **File Upload**: Can upload PNG/JPG/PDF files
2. ✅ **Response Handling**: Extracted data appears in form fields
3. ✅ **Preview Image**: Image preview works correctly
4. ✅ **Error Handling**: Proper error messages for invalid files
5. ✅ **Loading States**: Loading indicators work during processing
6. ✅ **Form Validation**: All form fields populate correctly

### 🔧 **Quick Debug Commands:**

Add these to your browser console for debugging:

```javascript
// Check API response structure
console.log('API Response:', response.data);

// Check if extracted_data exists
console.log('Extracted Data:', response.data.extracted_data);

// Check form state
console.log('Form Data:', formData);

// Check preview state
console.log('Preview Image:', previewImage);
```

### 🎯 **Expected Result After Fix:**

```javascript
// Console should show:
✅ Railway Processing Success: {
  filename: "done (1).jpg",
  mode: "demo", 
  extractedData: {
    no_faktur: "010.002-25.12345678",
    nama_lawan_transaksi: "PT. MULTI INTAN PERKASA",
    // ... other fields
  }
}

// Form fields should be populated
🧠 currentPage: 1
🖼️ preview_image: "/preview/done (1).jpg"  
🔍 Form fields populated with extracted data
```

### 🚨 **Critical Points:**

1. **Response Structure Changed**: `extracted_data` instead of direct fields
2. **Error Handling**: Check `status` field first
3. **File Preview**: Handle filename from response
4. **Demo Mode**: Backend currently returns demo data (mode: "demo")

**Setelah frontend diperbaiki, backend akan siap untuk implementasi real OCR!** 🚀
