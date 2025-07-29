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

def preprocess_for_ocr(image, engine="auto"):
    """
    Universal preprocessing function that works for both EasyOCR and Tesseract
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # General-purpose optimization that works well for both engines
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Noise reduction
    denoised = cv2.medianBlur(enhanced, 3)
    
    # Sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    return sharpened
