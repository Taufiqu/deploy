# utils/extraction/dpp.py

import re
from shared_utils.text_utils import clean_number

def extract_dpp(raw_text):
    """
    Extract DPP (Dasar Pengenaan Pajak)
    """
    try:
        dpp = 0.0
        dpp_str = ""
        override_ppn = None
        override_ppn_str = ""

        lines = raw_text.splitlines()
        for line in lines:
            if "dasar pengenaan pajak" in line.lower():
                numbers = re.findall(r"[\d.,]+", line)
                if numbers:
                    last_number = numbers[-1]
                    dpp = clean_number(last_number)
                    dpp_str = f"{dpp:,.2f}"
                    print(f"[✅ DPP dari baris] {dpp:,.2f} ← {line}")
                    break

        # Ambil semua angka besar sebagai kandidat
        all_numbers = re.findall(r"[\d.]{1,3}(?:[.,]\d{3}){2,}", raw_text)
        candidates = [clean_number(n) for n in all_numbers if clean_number(n) > 10_000_000]

        if dpp > 0:
            return dpp, dpp_str, override_ppn, override_ppn_str
        
        # Fallback ke kandidat terbesar
        if candidates:
            fallback = max(candidates)
            print(f"[⚠️ Fallback DPP] {fallback:,.2f}")
            return fallback, f"{fallback:,.2f}", override_ppn, override_ppn_str

        return 0.0, "0.00", override_ppn, override_ppn_str

    except Exception as e:
        print(f"[ERROR extract_dpp] {e}")
        return 0.0, "0.00", None, ""
