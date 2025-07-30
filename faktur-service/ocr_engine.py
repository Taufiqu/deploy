"""
OCR Engine untuk Faktur Processing - Railway Production
Berdasarkan proven implementation dari proyek-pajak-backend-clean
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
from thefuzz import fuzz

logger = logging.getLogger(__name__)

class FakturOCR:
    def __init__(self):
        # Set Tesseract path untuk Railway
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
    def preprocess_for_tesseract(self, image):
        """
        Preprocessing optimized untuk Tesseract OCR
        Berdasarkan shared_utils.image_utils.preprocess_for_tesseract
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
    
    def extract_text_from_image(self, image):
        """Extract text menggunakan Tesseract OCR dengan config optimal"""
        try:
            # Convert PIL to OpenCV format
            if isinstance(image, Image.Image):
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                img_cv = image
            
            # Apply preprocessing
            processed_img = self.preprocess_for_tesseract(img_cv)
            
            # OCR dengan config optimal (berdasarkan working repo)
            raw_text = pytesseract.image_to_string(
                processed_img, 
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
    
    def extract_faktur_tanggal(self, raw_text):
        """
        Extract nomor faktur dan tanggal dari raw text
        Berdasarkan faktur.utils.extraction.faktur_tanggal
        """
        no_faktur = None
        tanggal_obj = None

        logger.info("[🧾 DEBUG OCR Input] ------------")
        logger.info(raw_text[:500] + "..." if len(raw_text) > 500 else raw_text)
        logger.info("--------------------------------------")

        # 1. Extract Nomor Faktur dengan tolerant pattern
        tolerant_pattern = r"0[0-9a-zA-Z]{2}[-.\s]?[0-9a-zA-Z]{3}[-.\s]?[0-9a-zA-Z]{2}[-.\s]?[0-9a-zA-Z]{8,}"
        all_candidates = re.findall(tolerant_pattern, raw_text, re.IGNORECASE)
        logger.info(f"[DEBUG] Semua kandidat ditemukan: {all_candidates}")

        valid_candidates = []
        if all_candidates:
            lines = raw_text.splitlines()
            for cand in all_candidates:
                is_npwp = False
                for line in lines:
                    if cand in line:
                        if "npwp" in line.lower() or "nitku" in line.lower():
                            is_npwp = True
                            logger.info(f"[DEBUG] Kandidat '{cand}' dibuang karena berada di baris NPWP/NITKU.")
                            break
                if not is_npwp:
                    valid_candidates.append(cand)

        logger.info(f"[DEBUG] Kandidat yang valid setelah disaring: {valid_candidates}")

        # Metode toleran untuk memperbaiki OCR
        if not no_faktur and valid_candidates:
            logger.info("[DEBUG] Mencoba metode toleran untuk memperbaiki OCR...")

            candidate_str = valid_candidates[0]
            logger.info(f"[DEBUG] Kandidat faktur (toleran): {candidate_str}")

            # Normalisasi: Ganti huruf yang salah baca menjadi angka
            corrections = {
                "O": "0", "o": "0", "I": "1", "i": "1", "l": "1", "t": "1",
                "S": "5", "s": "5", "E": "6", "e": "6", "B": "8", "g": "9",
            }
            normalized_str = candidate_str
            for char, digit in corrections.items():
                normalized_str = normalized_str.replace(char, digit)

            logger.info(f"[DEBUG] Kandidat setelah normalisasi: {normalized_str}")

            # Ekstrak digit dan format
            digits_only = re.sub(r"\D", "", normalized_str)[:16]
            if len(digits_only) >= 14:
                nf = digits_only[:16]
                no_faktur = f"{nf[:3]}.{nf[3:6]}-{nf[6:8]}.{nf[8:]}"
                logger.info(f"[✅ DEBUG] Nomor faktur ditemukan (Metode Toleran): {no_faktur}")

        # Fallback dengan regex ketat
        if not no_faktur:
            normalized_text = raw_text.replace(",", ".").replace('"', '"')
            kandidat_faktur = re.findall(r"\d{3}[.\s]?\d{3}[-.\s]?\d{2}[.\s]?\d{8}", normalized_text)
            kandidat_faktur = [re.sub(r"\s+", "", k) for k in kandidat_faktur]

            if kandidat_faktur:
                no_faktur = max(kandidat_faktur, key=len)
                logger.info(f"[✅ DEBUG] Nomor faktur ditemukan: {no_faktur}")

        # 2. Extract Tanggal dengan multiple patterns
        bulan_list = "Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember"
        pola_tanggal_indonesia = rf"(\d{{1,2}})\s+({bulan_list})\s+(\d{{4}})"

        matches = re.findall(pola_tanggal_indonesia, raw_text, re.IGNORECASE)
        if matches:
            # Ambil temuan terakhir (biasanya yang paling benar di dekat ttd)
            hari, bulan, tahun = matches[-1]
            bulan_map = {
                "januari": "January", "februari": "February", "maret": "March", "april": "April",
                "mei": "May", "juni": "June", "juli": "July", "agustus": "August",
                "september": "September", "oktober": "October", "november": "November", "desember": "December",
            }
            bulan_inggris = bulan_map.get(bulan.lower())
            if bulan_inggris:
                try:
                    tanggal_obj = datetime.strptime(f"{hari} {bulan_inggris} {tahun}", "%d %B %Y")
                    logger.info(f"[DEBUG] Tanggal ditemukan (Pola Indonesia): {tanggal_obj.strftime('%Y-%m-%d')}")
                except ValueError:
                    pass

        # Fallback patterns untuk tanggal
        if not tanggal_obj:
            tanggal_match_dmY = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", raw_text)
            if tanggal_match_dmY:
                try:
                    tanggal_str = tanggal_match_dmY.group(0).replace("/", "-")
                    tanggal_obj = datetime.strptime(tanggal_str, "%d-%m-%Y")
                    logger.info(f"[DEBUG] Tanggal ditemukan (Pola DD-MM-YYYY): {tanggal_obj.strftime('%Y-%m-%d')}")
                except ValueError:
                    pass

        if not tanggal_obj:
            tanggal_match_Ymd = re.search(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", raw_text)
            if tanggal_match_Ymd:
                try:
                    tanggal_str = tanggal_match_Ymd.group(0).replace("/", "-")
                    tanggal_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")
                    logger.info(f"[DEBUG] Tanggal ditemukan (Pola YYYY-MM-DD): {tanggal_obj.strftime('%Y-%m-%d')}")
                except ValueError:
                    pass

        return no_faktur, tanggal_obj

    def clean_number(self, number_str):
        """Parse number string ke float"""
        try:
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[^\d.,]', '', str(number_str))
            
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

    def extract_dpp(self, raw_text):
        """
        Extract DPP (Dasar Pengenaan Pajak)
        Berdasarkan faktur.utils.extraction.dpp
        """
        try:
            dpp = 0.0
            dpp_line = ""

            lines = raw_text.splitlines()
            for line in lines:
                if "dasar pengenaan pajak" in line.lower():
                    numbers = re.findall(r"[\d.,]+", line)
                    if numbers:
                        last_number = numbers[-1]
                        dpp = self.clean_number(last_number)
                        dpp_line = line
                        logger.info(f"[✅ DPP dari baris] {dpp:,.2f} ← {line}")
                        break

            # Ambil semua angka besar sebagai kandidat
            all_numbers = re.findall(r"[\d.]{1,3}(?:[.,]\d{3}){2,}", raw_text)
            candidates = [self.clean_number(n) for n in all_numbers if self.clean_number(n) > 10_000_000]

            if dpp > 0:
                return dpp
            
            # Fallback ke kandidat terbesar
            if candidates:
                fallback = max(candidates)
                logger.info(f"[⚠️ Fallback DPP] {fallback:,.2f}")
                return fallback

            return 0.0

        except Exception as e:
            logger.error(f"[ERROR extract_dpp] {e}")
            return 0.0

    def extract_npwp_nama_rekanan(self, blok_rekanan):
        """Extract NPWP dan nama dari blok rekanan"""
        try:
            # Extract NPWP patterns
            npwp_patterns = [
                r'([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\.?[0-9]-[0-9]{3}\.?[0-9]{3})',
                r'([0-9]{15})'
            ]
            
            npwp = ""
            for pattern in npwp_patterns:
                match = re.search(pattern, blok_rekanan)
                if match:
                    npwp = match.group(1)
                    # Format NPWP
                    if len(npwp) >= 15:
                        digits = re.sub(r'\D', '', npwp)
                        if len(digits) >= 15:
                            npwp = f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}.{digits[8]}-{digits[9:12]}.{digits[12:15]}"
                    break
            
            # Extract nama perusahaan
            nama = ""
            company_patterns = [
                r'(?:PT\.?\s+|CV\.?\s+|UD\.?\s+|TOKO\s+)([A-Z\s&]+?)(?=\n|NPWP|ALAMAT|TLP)',
                r'PT\.?\s+([A-Z\s&]+)',
            ]
            
            for pattern in company_patterns:
                match = re.search(pattern, blok_rekanan.upper())
                if match:
                    nama = match.group(1).strip()
                    if len(nama) > 3:
                        break
            
            return nama, npwp
            
        except Exception as e:
            logger.error(f"[ERROR extract_npwp_nama] {e}")
            return "", ""

    def extract_keterangan(self, raw_text):
        """
        Extract keterangan dari raw text
        Berdasarkan faktur.utils.extraction.keterangan
        """
        try:
            start_match = re.search(r"Nama\s+Barang\s+Kena\s+Pajak.*?", raw_text, re.IGNORECASE)
            end_match = re.search(r"Dasar\s+Pengenaan\s+Pajak", raw_text, re.IGNORECASE)

            if not start_match or not end_match:
                return "Tidak ditemukan"

            block = raw_text[start_match.end() : end_match.start()]
            lines = [line.strip() for line in block.splitlines() if line.strip()]

            cleaned_lines = []
            seen_lines = set()

            # Kata-kata noise umum dari OCR
            noise_words = {"oh", "ka", "bah", "iai", "aa", "tr", "id", "na", "in", "5", "2", "3", "4", "es", "po", "sz"}
            
            # Typo corrections
            typo_map = {
                "DECA R": "DECANTER", "DESAND YCLON": "DESANDING CYCLONE",
                "PESIFIKA -SUA": "SPESIFIKASI SESUAI", "MATERI Tera": "MATERIAL",
                "MATER INSTALASI": "MATERIAL INSTALASI", "ikurangi": "Dikurangi",
            }

            for line in lines:
                if line in seen_lines:
                    continue
                seen_lines.add(line)

                # Normalisasi dasar
                line = re.sub(r"[^\w\s.,:;/\-()Rp]", "", line).strip()

                # Koreksi typo
                for typo, correct in typo_map.items():
                    if typo in line:
                        line = line.replace(typo, correct)

                # Hilangkan token noise
                tokens = [tok for tok in line.split() if tok.lower() not in noise_words]
                if not tokens:
                    continue

                # Gabung ulang dan tambahkan separator
                cleaned_line = " ".join(tokens).strip()
                if cleaned_line:
                    cleaned_lines.append(cleaned_line)

            return " || ".join(cleaned_lines) if cleaned_lines else "Tidak ditemukan"

        except Exception as e:
            logger.error(f"[ERROR extract_keterangan] {e}")
            return "Tidak ditemukan"

    def extract_jenis_pajak(self, raw_text, pt_utama="PT UTAMA"):
        """
        Extract jenis pajak (masukan/keluaran)
        Berdasarkan faktur.utils.extraction.jenis_pajak
        """
        try:
            logger.info("[DEBUG] Mulai extract_jenis_pajak...")
            
            def clean_string(s):
                return re.sub(r'[^\w\s]', '', s).strip().upper()
            
            pt_clean = clean_string(pt_utama)

            # Split berdasarkan "Pembeli Kena Pajak"
            splitter_pattern = r"Pembeli\s+(?:Barang\s+)?Kena\s+Pajak"
            parts = re.split(splitter_pattern, raw_text, flags=re.IGNORECASE)

            if len(parts) < 2:
                logger.info("[DEBUG] ❌ Bagian 'Pembeli Kena Pajak' tidak ditemukan, fallback ke full text.")
                for line in raw_text.splitlines():
                    if fuzz.ratio(clean_string(line), pt_clean) > 80:
                        logger.info(f"[DEBUG] ✅ Ditemukan nama PT utama di full text → PPN MASUKAN")
                        return "PPN_MASUKAN", "", raw_text
                logger.info("[DEBUG] ❌ Nama PT utama tidak ditemukan di fallback.")
                return None, None, None

            blok_penjual, blok_pembeli = parts
            logger.info("[DEBUG] Bagian pembeli dan penjual ditemukan.")

            for line in blok_pembeli.splitlines():
                if fuzz.ratio(clean_string(line), pt_clean) > 70:
                    logger.info(f"[DEBUG] ✅ Nama PT cocok di blok pembeli: {line}")
                    return "PPN_MASUKAN", blok_penjual, blok_pembeli

            for line in blok_penjual.splitlines():
                if fuzz.ratio(clean_string(line), pt_clean) > 70:
                    logger.info(f"[DEBUG] ✅ Nama PT cocok di blok penjual: {line}")
                    return "PPN_KELUARAN", blok_pembeli, blok_penjual

            logger.info("[DEBUG] ❌ Nama PT tidak cocok di kedua blok.")
            return None, None, None
            
        except Exception as e:
            logger.error(f"[ERROR extract_jenis_pajak] {e}")
            return None, None, None

    def parse_faktur_data(self, text):
        """Parse extracted text menjadi structured data dengan extraction modules"""
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
            
            # Extract nomor faktur dan tanggal
            no_faktur, tanggal_obj = self.extract_faktur_tanggal(text)
            
            if no_faktur:
                extracted_data["no_faktur"] = no_faktur
            
            if tanggal_obj:
                extracted_data["tanggal"] = tanggal_obj.strftime("%Y-%m-%d")
                extracted_data["bulan"] = tanggal_obj.strftime("%B %Y")
            else:
                extracted_data["tanggal"] = "2025-01-15"
                extracted_data["bulan"] = "Januari 2025"
            
            # Extract jenis pajak dan blok rekanan
            jenis_pajak, blok_rekanan, _ = self.extract_jenis_pajak(text, "PT UTAMA")
            
            if blok_rekanan:
                nama_rekanan, npwp_rekanan = self.extract_npwp_nama_rekanan(blok_rekanan)
                extracted_data["nama_lawan_transaksi"] = nama_rekanan or "PERUSAHAAN REKANAN"
                extracted_data["npwp_lawan_transaksi"] = npwp_rekanan or "00.000.000.0-000.000"
            
            # Extract DPP
            dpp = self.extract_dpp(text)
            extracted_data["dpp"] = dpp
            
            # Calculate PPN (11% of DPP)
            if dpp > 0:
                extracted_data["ppn"] = round(dpp * 0.11, 2)
            
            # Extract keterangan
            keterangan = self.extract_keterangan(text)
            extracted_data["keterangan"] = keterangan
            
            # Calculate confidence based on extracted fields
            confidence = self.calculate_confidence(extracted_data)
            
            logger.info(f"✅ Faktur parsing completed with confidence: {confidence}")
            return extracted_data, confidence
            
        except Exception as e:
            logger.error(f"❌ Faktur parsing failed: {e}")
            return None, 0.0
    
    def calculate_confidence(self, data):
        """Calculate confidence score based on extracted data quality"""
        score = 0.0
        
        # Check each field quality
        if data["no_faktur"] and len(data["no_faktur"]) >= 10:
            score += 0.25
        if data["tanggal"] and data["tanggal"] != "2025-01-15":
            score += 0.15
        if data["nama_lawan_transaksi"] and len(data["nama_lawan_transaksi"]) > 3 and data["nama_lawan_transaksi"] != "PERUSAHAAN REKANAN":
            score += 0.20
        if data["npwp_lawan_transaksi"] and len(data["npwp_lawan_transaksi"]) >= 15 and data["npwp_lawan_transaksi"] != "00.000.000.0-000.000":
            score += 0.15
        if data["dpp"] > 0:
            score += 0.20
        if data["keterangan"] and data["keterangan"] != "Extracted from OCR" and data["keterangan"] != "Tidak ditemukan":
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
