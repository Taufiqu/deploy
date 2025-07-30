# utils/extraction/npwp_nama.py

import re

def extract_npwp_nama_rekanan(blok_rekanan):
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
        print(f"[ERROR extract_npwp_nama] {e}")
        return "", ""
