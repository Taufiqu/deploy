# utils/extraction/ppn.py

import re
from shared_utils.text_utils import clean_number

def extract_ppn(raw_text, dpp, override_ppn=None):
    """
    Extract PPN atau calculate dari DPP
    """
    try:
        if override_ppn is not None:
            ppn = override_ppn
            ppn_str = f"{ppn:,.2f}"
            return ppn, ppn_str
        
        # Calculate PPN (11% of DPP)
        if dpp > 0:
            ppn = round(dpp * 0.11, 2)
            ppn_str = f"{ppn:,.2f}"
            print(f"[✅ PPN calculated] {ppn:,.2f} (11% dari DPP: {dpp:,.2f})")
            return ppn, ppn_str
        
        # Try to extract PPN from text
        lines = raw_text.splitlines()
        for line in lines:
            if "ppn" in line.lower() and "pajak pertambahan nilai" in line.lower():
                numbers = re.findall(r"[\d.,]+", line)
                if numbers:
                    last_number = numbers[-1]
                    ppn = clean_number(last_number)
                    ppn_str = f"{ppn:,.2f}"
                    print(f"[✅ PPN dari baris] {ppn:,.2f} ← {line}")
                    return ppn, ppn_str
        
        return 0.0, "0.00"

    except Exception as e:
        print(f"[ERROR extract_ppn] {e}")
        return 0.0, "0.00"
