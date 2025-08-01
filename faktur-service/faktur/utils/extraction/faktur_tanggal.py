# utils/extraction/faktur_tanggal.py

import re
from datetime import datetime

def extract_faktur_tanggal(raw_text):
    no_faktur = None
    tanggal_obj = None

    print("[🧾 DEBUG OCR Input] ------------")
    print(raw_text[:500] + "..." if len(raw_text) > 500 else raw_text)
    print("--------------------------------------")

    # 1. Cari semua teks yang polanya mirip nomor faktur di seluruh dokumen.
    tolerant_pattern = r"0[0-9a-zA-Z]{2}[-.\s]?[0-9a-zA-Z]{3}[-.\s]?[0-9a-zA-Z]{2}[-.\s]?[0-9a-zA-Z]{8,}"
    all_candidates = re.findall(tolerant_pattern, raw_text, re.IGNORECASE)
    print(f"[DEBUG] Semua kandidat ditemukan: {all_candidates}")

    valid_candidates = []
    if all_candidates:
        lines = raw_text.splitlines()
        for cand in all_candidates:
            is_npwp = False
            for line in lines:
                if cand in line:
                    if "npwp" in line.lower() or "nitku" in line.lower():
                        is_npwp = True
                        print(
                            f"[DEBUG] Kandidat '{cand}' dibuang karena berada di baris NPWP/NITKU."
                        )
                        break
            if not is_npwp:
                valid_candidates.append(cand)

    print(f"[DEBUG] Kandidat yang valid setelah disaring: {valid_candidates}")

    # Percobaan 2: Jika metode ketat gagal, baru jalankan metode toleran sebagai fallback.
    if not no_faktur and valid_candidates:
        print(
            "[DEBUG] Mencoba metode toleran untuk memperbaiki OCR..."
        )

        candidate_str = valid_candidates[0]
        print(f"[DEBUG] Kandidat faktur (toleran): {candidate_str}")

        # Normalisasi: Ganti huruf yang salah baca menjadi angka
        corrections = {
            "O": "0",
            "o": "0",
            "I": "1",
            "i": "1",
            "l": "1",
            "t": "1",
            "S": "5",
            "s": "5",
            "E": "6",
            "e": "6",
            "B": "8",
            "g": "9",
        }
        normalized_str = candidate_str
        for char, digit in corrections.items():
            normalized_str = normalized_str.replace(char, digit)

        print(f"[DEBUG] Kandidat setelah normalisasi: {normalized_str}")

        # Ekstrak digit dan format
        digits_only = re.sub(r"\D", "", normalized_str)[:16]
        if len(digits_only) >= 14:
            nf = digits_only[:16]
            no_faktur = f"{nf[:3]}.{nf[3:6]}-{nf[6:8]}.{nf[8:]}"
            print(f"[✅ DEBUG] Nomor faktur ditemukan (Metode Toleran): {no_faktur}")

    # Fallback: Metode ketat jika ada
    if not no_faktur:
        normalized_text = raw_text.replace(",", ".").replace('"', '"')
        kandidat_faktur = re.findall(r"\d{3}[.\s]?\d{3}[-.\s]?\d{2}[.\s]?\d{8}", normalized_text)
        kandidat_faktur = [re.sub(r"\s+", "", k) for k in kandidat_faktur]

        if kandidat_faktur:
            no_faktur = max(kandidat_faktur, key=len)
            print(f"[✅ DEBUG] Nomor faktur ditemukan: {no_faktur}")

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
                print(f"[DEBUG] Tanggal ditemukan (Pola Indonesia): {tanggal_obj.strftime('%Y-%m-%d')}")
            except ValueError:
                pass

    # Fallback patterns untuk tanggal
    if not tanggal_obj:
        tanggal_match_dmY = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", raw_text)
        if tanggal_match_dmY:
            try:
                tanggal_str = tanggal_match_dmY.group(0).replace("/", "-")
                tanggal_obj = datetime.strptime(tanggal_str, "%d-%m-%Y")
                print(f"[DEBUG] Tanggal ditemukan (Pola DD-MM-YYYY): {tanggal_obj.strftime('%Y-%m-%d')}")
            except ValueError:
                pass

    if not tanggal_obj:
        tanggal_match_Ymd = re.search(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", raw_text)
        if tanggal_match_Ymd:
            try:
                tanggal_str = tanggal_match_Ymd.group(0).replace("/", "-")
                tanggal_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")
                print(f"[DEBUG] Tanggal ditemukan (Pola YYYY-MM-DD): {tanggal_obj.strftime('%Y-%m-%d')}")
            except ValueError:
                pass

    return no_faktur, tanggal_obj
