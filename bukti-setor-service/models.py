# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PpnMasukan(db.Model):
    __tablename__ = "ppn_masukan"

    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    keterangan = db.Column(db.Text, nullable=True)
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
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'keterangan': self.keterangan,
            'npwp_lawan_transaksi': self.npwp_lawan_transaksi,
            'nama_lawan_transaksi': self.nama_lawan_transaksi,
            'no_faktur': self.no_faktur,
            'dpp': float(self.dpp),
            'ppn': float(self.ppn),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<PpnMasukan {self.no_faktur}>'

class PpnKeluaran(db.Model):
    __tablename__ = "ppn_keluaran"

    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    keterangan = db.Column(db.Text, nullable=True)
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
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'keterangan': self.keterangan,
            'npwp_lawan_transaksi': self.npwp_lawan_transaksi,
            'nama_lawan_transaksi': self.nama_lawan_transaksi,
            'no_faktur': self.no_faktur,
            'dpp': float(self.dpp),
            'ppn': float(self.ppn),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<PpnKeluaran {self.no_faktur}>'

class BuktiSetor(db.Model):
    __tablename__ = 'bukti_setor'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    kode_setor = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'kode_setor': self.kode_setor,
            'jumlah': float(self.jumlah),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<BuktiSetor {self.kode_setor}>'