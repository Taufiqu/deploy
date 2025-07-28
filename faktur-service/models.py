# ========================================
# DATABASE MODELS - FAKTUR SERVICE
# ========================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# ========================================
# PPN MASUKAN MODEL (Input Tax)
# ========================================
class PPNMasukan(db.Model):
    __tablename__ = 'ppn_masukan'
    
    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    keterangan = db.Column(db.Text)
    npwp_lawan_transaksi = db.Column(db.String(100), nullable=False)
    nama_lawan_transaksi = db.Column(db.String(255), nullable=False)
    no_faktur = db.Column(db.String(100), unique=True, nullable=False)
    dpp = db.Column(db.Numeric(15, 2), nullable=False)
    ppn = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bulan': self.bulan,
            'tanggal': self.tanggal.strftime('%Y-%m-%d') if self.tanggal else None,
            'keterangan': self.keterangan,
            'npwp_lawan_transaksi': self.npwp_lawan_transaksi,
            'nama_lawan_transaksi': self.nama_lawan_transaksi,
            'no_faktur': self.no_faktur,
            'dpp': float(self.dpp) if self.dpp else 0,
            'ppn': float(self.ppn) if self.ppn else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ========================================
# PPN KELUARAN MODEL (Output Tax)
# ========================================
class PPNKeluaran(db.Model):
    __tablename__ = 'ppn_keluaran'
    
    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    keterangan = db.Column(db.Text)
    npwp_lawan_transaksi = db.Column(db.String(100), nullable=False)
    nama_lawan_transaksi = db.Column(db.String(255), nullable=False)
    no_faktur = db.Column(db.String(100), unique=True, nullable=False)
    dpp = db.Column(db.Numeric(15, 2), nullable=False)
    ppn = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bulan': self.bulan,
            'tanggal': self.tanggal.strftime('%Y-%m-%d') if self.tanggal else None,
            'keterangan': self.keterangan,
            'npwp_lawan_transaksi': self.npwp_lawan_transaksi,
            'nama_lawan_transaksi': self.nama_lawan_transaksi,
            'no_faktur': self.no_faktur,
            'dpp': float(self.dpp) if self.dpp else 0,
            'ppn': float(self.ppn) if self.ppn else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
