#backend/bukti_setor/routes.py
# ==============================================================================
# File: backend/bukti_setor/routes.py
# Deskripsi: Rute untuk mengelola bukti setor, termasuk upload, proses,
# penyimpanan, dan pengambilan data bukti setor.
# ==============================================================================

import os
import traceback
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from datetime import datetime
from models import BuktiSetor, db

# shared_utils
from shared_utils.text_utils import clean_transaction_value
from shared_utils.file_utils import allowed_file, is_valid_image

# local utils
from bukti_setor.utils.bukti_setor_processor import extract_bukti_setor_data
from bukti_setor.utils.parsing.kode_setor import parse_kode_setor
from bukti_setor.utils.parsing.tanggal import parse_tanggal
from bukti_setor.utils.parsing.jumlah import parse_jumlah
from bukti_setor.utils.helpers import simpan_preview_image      
from bukti_setor.services.delete import delete_bukti_setor
from bukti_setor.services.excel_exporter_bukti_setor import generate_excel_bukti_setor_export  
# ==============================================================================
# Blueprints
bukti_setor_bp = Blueprint('bukti_setor', __name__, url_prefix='/api/bukti_setor')
laporan_bp = Blueprint("laporan_bp", __name__)

# ========== ENDPOINT: PREVIEW GAMBAR ==========
@bukti_setor_bp.route('/uploads/<path:filename>')
def serve_preview(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)

@bukti_setor_bp.route('/process', methods=['POST'])
def process_bukti_setor_endpoint():
    print("🚀 [DEBUG] Starting process_bukti_setor_endpoint")
    
    if 'file' not in request.files:
        print("❌ [DEBUG] No file in request")
        return jsonify(error="File tidak ditemukan"), 400
    
    file = request.files['file']
    print(f"📁 [DEBUG] Processing file: {file.filename}")
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, file.filename)
    print(f"💾 [DEBUG] Saving file to: {filepath}")
    
    file.save(filepath)
    print(f"✅ [DEBUG] File saved successfully")

    try:
        poppler_path = current_app.config.get('POPPLER_PATH')
        print(f"🔧 [DEBUG] Poppler path: {poppler_path}")
        
        extracted_data = extract_bukti_setor_data(filepath, poppler_path)
        print(f"📊 [DEBUG] Extracted data: {extracted_data}")
        
        # TEMPORARY FIX: Return only the results array if frontend expects it
        # Frontend seems to be reading response.data directly as array
        if extracted_data.get('success') and 'results' in extracted_data:
            print(f"📤 [DEBUG] Returning results array directly: {extracted_data['results']}")
            return jsonify(extracted_data['results']), 200
        else:
            print(f"📤 [DEBUG] Returning full extracted_data")
            return jsonify(extracted_data), 200
    except Exception as e:
        print(f"❌ [DEBUG] Exception occurred: {str(e)}")
        current_app.logger.error(f"Error processing bukti setor: {e}\n{traceback.format_exc()}")
        return jsonify(error=str(e)), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️ [DEBUG] Cleanup: file {filepath} removed")

# ========== ENDPOINT: SIMPAN KE DB ==========
@bukti_setor_bp.route('/save', methods=['POST'])
def save_bukti_setor_endpoint():
    data = request.get_json()
    print("🚀 Data diterima di backend:", data)

    try:
        # Support untuk bulk save (multiple records)
        if isinstance(data, list):
            saved_count = 0
            for item in data:
                kode_setor = item.get('kode_setor')
                tanggal = item.get('tanggal')
                jumlah = item.get('jumlah')

                if not all([kode_setor, tanggal, jumlah]):
                    print(f"⚠️ Skipping incomplete record: {item}")
                    continue

                tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d').date()
                new_record = BuktiSetor(
                    tanggal=tanggal_obj,
                    kode_setor=str(kode_setor),
                    jumlah=float(jumlah)
                )
                db.session.add(new_record)
                saved_count += 1
            
            db.session.commit()
            return jsonify(message=f"{saved_count} bukti setor berhasil disimpan!"), 201
        
        # Single record save
        else:
            kode_setor = data.get('kode_setor')
            tanggal = data.get('tanggal')
            jumlah = data.get('jumlah')

            if not all([kode_setor, tanggal, jumlah]):
                return jsonify(error="Field tidak lengkap"), 400

            tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d').date()
            new_record = BuktiSetor(
                tanggal=tanggal_obj,
                kode_setor=str(kode_setor),
                jumlah=float(jumlah)
            )
            db.session.add(new_record)
            db.session.commit()
            return jsonify(message="Data bukti setor berhasil disimpan!"), 201
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving bukti setor: {e}\n{traceback.format_exc()}")
        return jsonify(error=f"Kesalahan saat menyimpan: {str(e)}"), 500

# ========== ENDPOINT: AMBIL DATA HISTORY ==========
@bukti_setor_bp.route('/history', methods=['GET'])
def get_bukti_setor_history():
    try:
        results = db.session.execute(db.select(BuktiSetor).order_by(BuktiSetor.tanggal.desc())).scalars().all()
        data = [{
            "id": row.id,
            "kode_setor": row.kode_setor,
            "tanggal": row.tanggal.strftime("%Y-%m-%d"),
            "jumlah": float(row.jumlah),
            "created_at": row.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for row in results]
        return jsonify(message="Data berhasil diambil.", data=data), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching history: {e}\n{traceback.format_exc()}")
        return jsonify(error="Gagal mengambil data."), 500

# ========== ENDPOINT: DELETE DATA ==========
@bukti_setor_bp.route('/delete/<int:id>', methods=["DELETE"])
def delete_bukti_setor_route(id):
    return delete_bukti_setor(id)

# ========== ENDPOINT: EXPORT EXCEL ==========
@laporan_bp.route("/api/export_bukti_setor", methods=["GET"])
def export_bukti_setor():
    return generate_excel_bukti_setor_export(db)
