# ========================================
# DATABASE MODELS - BUKTI SETOR SERVICE
# ========================================

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# ========================================
# BUKTI SETOR MODEL (Tax Payment Receipt)
# ========================================
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
            'tanggal': self.tanggal.strftime('%Y-%m-%d') if self.tanggal else None,
            'kode_setor': self.kode_setor,
            'jumlah': float(self.jumlah) if self.jumlah else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
