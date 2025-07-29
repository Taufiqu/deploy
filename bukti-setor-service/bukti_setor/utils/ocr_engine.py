import os
import threading
import numpy as np
from PIL import Image

# Try to import EasyOCR, fallback to Tesseract
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Global variables for lazy loading
_ocr_reader = None
_ocr_lock = threading.Lock()
_ocr_engine = None

def detect_ocr_engine():
    """
    Detect available OCR engine and set preference
    """
    global _ocr_engine
    
    if _ocr_engine is None:
        if EASYOCR_AVAILABLE:
            _ocr_engine = "easyocr"
            print("🤖 Using EasyOCR engine")
        elif TESSERACT_AVAILABLE:
            _ocr_engine = "tesseract"
            print("🤖 Using Tesseract engine")
        else:
            raise ImportError("No OCR engine available. Install either easyocr or pytesseract.")
    
    return _ocr_engine

def get_easyocr_reader():
    """
    Lazy loading untuk EasyOCR Reader
    Hanya initialize ketika benar-benar dibutuhkan
    """
    global _ocr_reader
    
    if not EASYOCR_AVAILABLE:
        raise ImportError("EasyOCR not available")
    
    if _ocr_reader is None:
        with _ocr_lock:
            if _ocr_reader is None:  # Double-check locking pattern
                print("🤖 Inisialisasi EasyOCR Reader...")
                _ocr_reader = easyocr.Reader(['id', 'en'], gpu=False)
                print("✅ EasyOCR Reader berhasil diinisialisasi.")
    
    return _ocr_reader

def process_with_easyocr(image_array):
    """
    Process image dengan EasyOCR - lazy loaded
    """
    reader = get_easyocr_reader()
    results = reader.readtext(image_array)
    return results

def process_with_tesseract(image_array):
    """
    Process image dengan Tesseract OCR
    """
    if not TESSERACT_AVAILABLE:
        raise ImportError("Tesseract not available")
    
    # Convert numpy array to PIL Image if needed
    if isinstance(image_array, np.ndarray):
        image = Image.fromarray(image_array)
    else:
        image = image_array
    
    # Extract text using Tesseract with Indonesian and English
    custom_config = r'--oem 3 --psm 6 -l ind+eng'
    text = pytesseract.image_to_string(image, config=custom_config)
    
    # Format output similar to EasyOCR format: [(bbox, text, confidence)]
    # For simplicity, return the whole text as one result
    # In production, you might want to use pytesseract.image_to_data for more details
    if text.strip():
        return [([0, 0, 0, 0], text.strip(), 0.8)]  # Mock bbox and confidence
    else:
        return []

def process_with_ocr(image_array):
    """
    Universal OCR processing function that uses available engine
    """
    engine = detect_ocr_engine()
    
    try:
        if engine == "easyocr":
            return process_with_easyocr(image_array)
        elif engine == "tesseract":
            return process_with_tesseract(image_array)
        else:
            raise ValueError(f"Unknown OCR engine: {engine}")
    except Exception as e:
        print(f"❌ OCR processing failed with {engine}: {e}")
        # Try fallback if available
        if engine == "easyocr" and TESSERACT_AVAILABLE:
            print("🔄 Falling back to Tesseract...")
            return process_with_tesseract(image_array)
        elif engine == "tesseract" and EASYOCR_AVAILABLE:
            print("🔄 Falling back to EasyOCR...")
            return process_with_easyocr(image_array)
        else:
            raise
