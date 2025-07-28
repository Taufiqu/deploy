# 🔧 RAILWAY DEPLOYMENT TROUBLESHOOTING GUIDE
# =================================================

## ❌ MASALAH: Pip Install Failed (Exit Code 1)

### 🎯 PENYEBAB UMUM:
1. **PyTorch dependency conflict** (EasyOCR service)
2. **Missing system dependencies** 
3. **Version incompatibility**
4. **Memory limit saat build**

### ✅ SOLUSI YANG SUDAH DITERAPKAN:

#### 1. **Fixed Dockerfile Build Strategy:**
- ✅ Install PyTorch terpisah (CPU-only)
- ✅ Compatible version dependencies  
- ✅ Added missing system libraries
- ✅ Pip cache cleanup

#### 2. **Updated Requirements.txt:**
- ✅ **Faktur Service**: Tesseract-focused, lightweight
- ✅ **Bukti Setor Service**: EasyOCR-compatible versions
- ✅ Removed conflicting `--find-links` format

#### 3. **System Dependencies Added:**
```dockerfile
# Added to both services:
libgl1-mesa-glx libglib2.0-0 libgomp1 
libsm6 libxext6 libxrender-dev 
build-essential
```

### 🚀 RETRY DEPLOYMENT STEPS:

#### Option A: Use Standard Dockerfiles
1. **Deploy Faktur Service:**
   - Root Directory: `faktur-service`
   - Uses: `Dockerfile` (updated)
   - Build time: ~5-8 minutes

2. **Deploy Bukti Setor Service:**
   - Root Directory: `bukti-setor-service` 
   - Uses: `Dockerfile` (updated)
   - Build time: ~10-15 minutes (PyTorch download)

#### Option B: Use Alternative Dockerfile (If still fails)
```bash
# In Railway, set build command:
docker build -f Dockerfile.alternative -t app .
```

### 🔍 DEBUGGING RAILWAY BUILD:

#### 1. **Check Build Logs:**
- Railway Dashboard → Deployments → View Logs
- Look for specific pip error messages
- Check memory usage during build

#### 2. **Common Error Messages & Solutions:**

**Error:** `Could not find a version that satisfies...`
- ✅ **Fixed**: Updated to compatible versions

**Error:** `Failed building wheel for opencv-python`
- ✅ **Fixed**: Added build-essential, system libs

**Error:** `RuntimeError: Ninja is required to load C++ extensions`
- ✅ **Fixed**: Using opencv-python-headless (no build needed)

**Error:** `torch 2.1.0+cpu is not available`
- ✅ **Fixed**: Using torch 2.0.1+cpu (more stable)

### 📊 BUILD TIME EXPECTATIONS:

| Service | Expected Build Time | Dependencies |
|---------|-------------------|--------------|
| **Faktur** | 5-8 minutes | Tesseract, basic libs |
| **Bukti Setor** | 10-15 minutes | PyTorch, EasyOCR models |

### 🎯 IF BUILD STILL FAILS:

#### Plan B: Simplified Deployment
1. **Remove EasyOCR temporarily:**
   ```python
   # Comment out EasyOCR import in bukti_setor service
   # Use basic OCR or manual processing for testing
   ```

2. **Deploy Faktur service first** (simpler, should work)

3. **Debug Bukti Setor separately:**
   - Test locally with Docker
   - Use Railway's container registry
   - Deploy after confirmed working

### 🔄 CURRENT STATUS:
- ✅ **Dockerfiles**: Updated and optimized
- ✅ **Requirements**: Compatible versions
- ✅ **System deps**: All required libraries added
- ✅ **PyTorch**: Separate installation strategy

**▶️ READY TO RETRY DEPLOYMENT!**

---
## 📞 Quick Test Commands:

Test Faktur locally:
```bash
cd faktur-service
docker build -t faktur-test .
docker run -p 5001:5001 faktur-test
```

Test Bukti Setor locally:
```bash
cd bukti-setor-service  
docker build -t bukti-setor-test .
docker run -p 5002:5002 bukti-setor-test
```
