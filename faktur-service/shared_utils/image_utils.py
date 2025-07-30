# shared_utils/image_utils.py

import cv2
import numpy as np

def preprocess_for_tesseract(image):
    """
    Preprocessing optimized untuk Tesseract OCR
    Digunakan oleh faktur processing
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Tesseract-specific optimization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    denoised = cv2.medianBlur(enhanced, 3)
    
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    return sharpened

def preprocess_for_easyocr(image):
    """
    Preprocessing optimized untuk EasyOCR
    Digunakan oleh bukti_setor processing
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # EasyOCR-specific optimization
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Gaussian blur for EasyOCR
    blurred = cv2.GaussianBlur(enhanced, (1, 1), 0)
    
    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    
    return processed
