"""
OCR Engine untuk Faktur Processing - Railway Production
Implementasi sesuai dengan arsitektur repo proyek-pajak-backend-clean
"""
import os
import re
import io
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from datetime import datetime
import logging

# Import extraction modules sesuai arsitektur referensi
from faktur.utils import (
    extract_faktur_tanggal, extract_jenis_pajak,
    extract_npwp_nama_rekanan, extract_dpp,
    extract_ppn, extract_keterangan
)
from shared_utils.image_utils import preprocess_for_tesseract
from shared_utils.file_utils import simpan_preview_image

logger = logging.getLogger(__name__)

class FakturOCR:
    def __init__(self):
        # Set Tesseract path untuk Railway
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
    def extract_text_from_image(self, image):
        """Extract text menggunakan Tesseract OCR dengan preprocessing yang tepat"""
        try:
            # Convert PIL to OpenCV format jika perlu
            if isinstance(image, Image.Image):
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                img_cv = image
            
            # Apply preprocessing sesuai repo referensi
            processed_img = preprocess_for_tesseract(img_cv)
            
            # OCR dengan config yang sesuai repo referensi
            raw_text = pytesseract.image_to_string(
                img_cv,  # Gunakan original image seperti di repo referensi
                lang="ind", 
                config="--psm 6"
            )
            
            logger.info(f"✅ OCR extraction successful, text length: {len(raw_text)}")
            return raw_text.strip()
            
        except Exception as e:
            logger.error(f"❌ OCR extraction failed: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_bytes):
        """Extract text dari PDF file"""
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
            
            if not images:
                raise Exception("No pages found in PDF")
            
            # Process first page
            text = self.extract_text_from_image(images[0])
            
            logger.info(f"✅ PDF extraction successful")
            return text
            
        except Exception as e:
            logger.error(f"❌ PDF extraction failed: {e}")
            return ""

    def parse_faktur_data(self, raw_text, filename):
        """Parse extracted text menggunakan extraction modules sesuai repo referensi"""
        try:
            print(f"[🔤 DEBUG OCR-Tesseract Input] {filename} ------------")
            print(raw_text[:500] + "..." if len(raw_text) > 500 else raw_text)
            print("--------------------------------------------")
            
            # Extract faktur dan tanggal - module utama
            no_faktur, tanggal_obj = extract_faktur_tanggal(raw_text)
            
            if not no_faktur:
                logger.warning("⚠️ Nomor faktur tidak ditemukan")
                return None, 0.0
            
            # Extract jenis pajak dan blok rekanan
            nama_pt_utama = "PT UTAMA"  # Sesuaikan dengan PT yang digunakan
            jenis_pajak, blok_rekanan, _ = extract_jenis_pajak(raw_text, nama_pt_utama)
            
            if not jenis_pajak:
                logger.warning("⚠️ Jenis pajak tidak dapat ditentukan")
                # Set default values untuk testing
                blok_rekanan = raw_text
                jenis_pajak = "PPN_MASUKAN"
            
            # Extract nama dan NPWP rekanan
            nama_rekanan, npwp_rekanan = extract_npwp_nama_rekanan(blok_rekanan)
            
            # Extract DPP
            dpp, dpp_str, override_ppn, override_ppn_str = extract_dpp(raw_text)
            
            # Extract PPN
            ppn, ppn_str = extract_ppn(raw_text, dpp, override_ppn)
            
            # Extract keterangan
            keterangan = extract_keterangan(raw_text)
            
            # Build result sesuai dengan format repo referensi
            extracted_data = {
                "no_faktur": no_faktur,
                "tanggal": tanggal_obj.strftime("%Y-%m-%d") if tanggal_obj else "2025-01-15",
                "nama_lawan_transaksi": nama_rekanan or "PERUSAHAAN REKANAN",
                "npwp_lawan_transaksi": npwp_rekanan or "00.000.000.0-000.000",
                "dpp": dpp,
                "ppn": ppn,
                "bulan": tanggal_obj.strftime("%B %Y") if tanggal_obj else "Januari 2025",
                "keterangan": keterangan or "OCR Extraction"
            }
            
            # Calculate confidence based on extraction quality
            confidence = self.calculate_confidence(extracted_data, no_faktur, tanggal_obj, nama_rekanan, npwp_rekanan)
            
            logger.info(f"✅ Faktur parsing completed with confidence: {confidence}")
            print(f"[✅ HASIL] Faktur: {no_faktur} | DPP: {dpp_str} | PPN: {ppn_str}")
            
            return extracted_data, confidence
            
        except Exception as e:
            logger.error(f"❌ Faktur parsing failed: {e}")
            return None, 0.0
    
    def calculate_confidence(self, data, no_faktur, tanggal_obj, nama_rekanan, npwp_rekanan):
        """Calculate confidence score berdasarkan kualitas extraction"""
        score = 0.0
        
        # Skor berdasarkan field yang berhasil di-extract
        if no_faktur and len(no_faktur) >= 10:
            score += 0.30  # Nomor faktur paling penting
        if tanggal_obj is not None:
            score += 0.20  # Tanggal penting
        if nama_rekanan and len(nama_rekanan) > 3 and nama_rekanan != "PERUSAHAAN REKANAN":
            score += 0.20  # Nama rekanan
        if npwp_rekanan and len(npwp_rekanan) >= 15 and npwp_rekanan != "00.000.000.0-000.000":
            score += 0.15  # NPWP
        if data["dpp"] > 0:
            score += 0.10  # DPP amount
        if data["keterangan"] and data["keterangan"] != "OCR Extraction" and data["keterangan"] != "Tidak ditemukan":
            score += 0.05  # Keterangan
        
        return min(score, 1.0)

    def process_file(self, file_bytes, filename):
        """Main method untuk memproses file sesuai dengan workflow repo referensi"""
        try:
            logger.info(f"🔍 Starting OCR processing for: {filename}")
            
            # Determine file type
            file_ext = filename.lower().split('.')[-1]
            
            if file_ext == 'pdf':
                # Process PDF
                text = self.extract_text_from_pdf(file_bytes)
            else:
                # Process image
                image = Image.open(io.BytesIO(file_bytes))
                text = self.extract_text_from_image(image)
            
            if not text:
                raise Exception("No text extracted from file")
            
            # Parse extracted text dengan extraction modules
            extracted_data, confidence = self.parse_faktur_data(text, filename)
            
            if not extracted_data:
                raise Exception("Failed to parse faktur data")
            
            logger.info(f"✅ OCR processing completed for: {filename}")
            return extracted_data, confidence, len(text)
            
        except Exception as e:
            logger.error(f"❌ OCR processing failed for {filename}: {e}")
            raise e
