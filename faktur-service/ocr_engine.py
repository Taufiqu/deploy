"""
OCR Engine untuk Faktur Processing - Railway Production
"""
import os
import re
import io
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_bytes
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FakturOCR:
    def __init__(self):
        # Set Tesseract path untuk Railway
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
    def preprocess_image(self, image):
        """Preprocessing image untuk OCR yang lebih akurat"""
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply bilateral filter to reduce noise
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(
                filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Convert back to PIL
            processed_image = Image.fromarray(thresh)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(processed_image)
            processed_image = enhancer.enhance(1.5)
            
            # Enhance sharpness
            sharpener = ImageEnhance.Sharpness(processed_image)
            processed_image = sharpener.enhance(2.0)
            
            return processed_image
            
        except Exception as e:
            logger.warning(f"Preprocessing failed, using original: {e}")
            return image
    
    def extract_text_from_image(self, image):
        """Extract text menggunakan Tesseract OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # OCR configuration untuk dokumen Indonesia
            custom_config = r'--oem 3 --psm 6 -l ind+eng'
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            logger.info(f"✅ OCR extraction successful, text length: {len(text)}")
            return text.strip()
            
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
    
    def parse_faktur_data(self, text):
        """Parse extracted text menjadi structured data"""
        try:
            extracted_data = {
                "no_faktur": "",
                "tanggal": "",
                "nama_lawan_transaksi": "",
                "npwp_lawan_transaksi": "",
                "dpp": 0.0,
                "ppn": 0.0,
                "bulan": "",
                "keterangan": "Extracted from OCR"
            }
            
            # Clean text
            text = re.sub(r'\s+', ' ', text.strip())
            text_upper = text.upper()
            
            # Extract No. Faktur
            faktur_patterns = [
                r'(?:NO\.?\s*FAKTUR|FAKTUR\s*NO\.?|SERIAL\s*NUMBER)[\s:]*([0-9]{3}\.?[0-9]{3}-[0-9]{2}\.?[0-9]{8})',
                r'([0-9]{3}\.?[0-9]{3}-[0-9]{2}\.?[0-9]{8})',
                r'(?:FAKTUR|NO)[\s:]*([0-9]{10,})',
            ]
            
            for pattern in faktur_patterns:
                match = re.search(pattern, text_upper)
                if match:
                    extracted_data["no_faktur"] = match.group(1).replace(' ', '')
                    break
            
            # Extract Tanggal
            date_patterns = [
                r'(?:TANGGAL|DATE|TGL)[\s:]*([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
                r'([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
                r'([0-9]{1,2}\s+(?:JANUARI|FEBRUARI|MARET|APRIL|MEI|JUNI|JULI|AGUSTUS|SEPTEMBER|OKTOBER|NOVEMBER|DESEMBER)\s+[0-9]{4})'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text_upper)
                if match:
                    date_str = match.group(1)
                    extracted_data["tanggal"] = self.normalize_date(date_str)
                    break
            
            # Extract Nama Lawan Transaksi
            company_patterns = [
                r'(?:PT\.?\s+|CV\.?\s+|UD\.?\s+|TOKO\s+)([A-Z\s&]+?)(?=\n|NPWP|ALAMAT|TLP)',
                r'(?:KEPADA|NAMA|CUSTOMER)[\s:]+([A-Z\s&\.]+?)(?=\n|NPWP|ALAMAT)',
                r'PT\.?\s+([A-Z\s&]+)',
            ]
            
            for pattern in company_patterns:
                match = re.search(pattern, text_upper)
                if match:
                    company_name = match.group(1).strip()
                    if len(company_name) > 3:  # Filter out short matches
                        extracted_data["nama_lawan_transaksi"] = company_name
                        break
            
            # Extract NPWP
            npwp_patterns = [
                r'NPWP[\s:]*([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]-[0-9]{3}\.?[0-9]{3})',
                r'([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]-[0-9]{3}\.?[0-9]{3})',
                r'([0-9]{15})'
            ]
            
            for pattern in npwp_patterns:
                match = re.search(pattern, text_upper)
                if match:
                    npwp = match.group(1)
                    extracted_data["npwp_lawan_transaksi"] = self.format_npwp(npwp)
                    break
            
            # Extract DPP (Dasar Pengenaan Pajak)
            dpp_patterns = [
                r'(?:DPP|DASAR\s+PENGENAAN\s+PAJAK|SUBTOTAL)[\s:]*(?:RP\.?\s*)?([0-9.,]+)',
                r'(?:JUMLAH|TOTAL|SUBTOTAL)[\s:]*(?:RP\.?\s*)?([0-9.,]+)(?=\s*(?:\n|PPN|PPH))',
                r'(?:RP\.?\s*)?([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?)'
            ]
            
            for pattern in dpp_patterns:
                matches = re.findall(pattern, text_upper)
                if matches:
                    # Get the largest number (likely the DPP)
                    amounts = [self.parse_number(match) for match in matches]
                    amounts = [amt for amt in amounts if amt > 10000]  # Filter small amounts
                    if amounts:
                        extracted_data["dpp"] = max(amounts)
                        break
            
            # Calculate PPN (11% of DPP)
            if extracted_data["dpp"] > 0:
                extracted_data["ppn"] = round(extracted_data["dpp"] * 0.11, 2)
            
            # Extract/generate Bulan
            if extracted_data["tanggal"]:
                try:
                    date_obj = datetime.strptime(extracted_data["tanggal"], '%Y-%m-%d')
                    months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                             'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
                    extracted_data["bulan"] = f"{months[date_obj.month-1]} {date_obj.year}"
                except:
                    extracted_data["bulan"] = "Januari 2025"  # Fallback
            
            # Calculate confidence score based on extracted fields
            confidence = self.calculate_confidence(extracted_data)
            
            logger.info(f"✅ Faktur parsing completed with confidence: {confidence}")
            return extracted_data, confidence
            
        except Exception as e:
            logger.error(f"❌ Faktur parsing failed: {e}")
            return None, 0.0
    
    def normalize_date(self, date_str):
        """Normalize date string ke format YYYY-MM-DD"""
        try:
            # Handle different date formats
            date_str = date_str.strip()
            
            # DD/MM/YYYY or DD-MM-YYYY
            if re.match(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', date_str):
                parts = re.split(r'[-/]', date_str)
                day, month, year = parts[0], parts[1], parts[2]
                
                # Convert 2-digit year to 4-digit
                if len(year) == 2:
                    year = f"20{year}"
                
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Handle Indonesian month names
            month_map = {
                'JANUARI': '01', 'FEBRUARI': '02', 'MARET': '03', 'APRIL': '04',
                'MEI': '05', 'JUNI': '06', 'JULI': '07', 'AGUSTUS': '08',
                'SEPTEMBER': '09', 'OKTOBER': '10', 'NOVEMBER': '11', 'DESEMBER': '12'
            }
            
            for month_name, month_num in month_map.items():
                if month_name in date_str.upper():
                    parts = date_str.upper().split()
                    day = parts[0] if parts[0].isdigit() else '01'
                    year = parts[2] if len(parts) > 2 and parts[2].isdigit() else '2025'
                    return f"{year}-{month_num}-{day.zfill(2)}"
            
            return "2025-01-15"  # Fallback
            
        except:
            return "2025-01-15"  # Fallback
    
    def format_npwp(self, npwp):
        """Format NPWP ke format standard"""
        try:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', npwp)
            
            if len(digits) >= 15:
                # Format: XX.XXX.XXX.X-XXX.XXX
                return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}.{digits[8]}-{digits[9:12]}.{digits[12:15]}"
            
            return npwp  # Return original if can't format
            
        except:
            return npwp
    
    def parse_number(self, number_str):
        """Parse number string ke float"""
        try:
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[^\d.,]', '', number_str)
            
            # Handle Indonesian number format (1.000.000,00)
            if ',' in cleaned and '.' in cleaned:
                if cleaned.rfind(',') > cleaned.rfind('.'):
                    # Indonesian format
                    cleaned = cleaned.replace('.', '').replace(',', '.')
                else:
                    # US format
                    cleaned = cleaned.replace(',', '')
            elif ',' in cleaned:
                # Check if comma is decimal separator
                if len(cleaned.split(',')[-1]) <= 2:
                    cleaned = cleaned.replace(',', '.')
                else:
                    cleaned = cleaned.replace(',', '')
            
            return float(cleaned)
            
        except:
            return 0.0
    
    def calculate_confidence(self, data):
        """Calculate confidence score based on extracted data quality"""
        score = 0.0
        total_fields = 6
        
        # Check each field
        if data["no_faktur"] and len(data["no_faktur"]) >= 10:
            score += 0.25
        if data["tanggal"] and data["tanggal"] != "2025-01-15":
            score += 0.15
        if data["nama_lawan_transaksi"] and len(data["nama_lawan_transaksi"]) > 3:
            score += 0.20
        if data["npwp_lawan_transaksi"] and len(data["npwp_lawan_transaksi"]) >= 15:
            score += 0.15
        if data["dpp"] > 0:
            score += 0.20
        if data["bulan"] and data["bulan"] != "Januari 2025":
            score += 0.05
        
        return min(score, 1.0)

    def process_file(self, file_bytes, filename):
        """Main method untuk memproses file"""
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
            
            # Parse extracted text
            extracted_data, confidence = self.parse_faktur_data(text)
            
            if not extracted_data:
                raise Exception("Failed to parse faktur data")
            
            logger.info(f"✅ OCR processing completed for: {filename}")
            return extracted_data, confidence, len(text)
            
        except Exception as e:
            logger.error(f"❌ OCR processing failed for {filename}: {e}")
            raise e
