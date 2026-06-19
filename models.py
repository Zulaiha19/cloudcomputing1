from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Inisialisasi object SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """Tabel Pengguna untuk fitur Login dan Langganan SaaS."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Status langganan: 'Gratis' atau 'Premium'
    subscription_type = db.Column(db.String(50), default='Gratis')
    
    # Relasi ke catatan sholat
    prayer_logs = db.relationship('PrayerLog', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.email} - {self.subscription_type}>"

class PrayerLog(db.Model):
    """Tabel untuk menyimpan Tracker Sholat Harian pengguna."""
    __tablename__ = 'prayer_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    
    # Status checklist (True jika sudah sholat, False jika belum/lewat)
    fajr = db.Column(db.Boolean, default=False)
    dhuhr = db.Column(db.Boolean, default=False)
    asr = db.Column(db.Boolean, default=False)
    maghrib = db.Column(db.Boolean, default=False)
    isha = db.Column(db.Boolean, default=False)