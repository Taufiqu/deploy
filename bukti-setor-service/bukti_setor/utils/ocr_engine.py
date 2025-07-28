import easyocr
import threading

# Global variables for lazy loading
_ocr_reader = None
_ocr_lock = threading.Lock()

def get_easyocr_reader():
    """
    Lazy loading untuk EasyOCR Reader
    Hanya initialize ketika benar-benar dibutuhkan
    """
    global _ocr_reader
    
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
