import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

class Config:
    """Kelas untuk menyimpan semua konfigurasi aplikasi."""
    
    # Keamanan dan Database
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_jika_env_kosong")
    # Jika gagal konek MySQL, otomatis menggunakan SQLite (untuk testing awal)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///sholatpro_local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfigurasi API Aladhan
    BASE_URL = os.getenv("BASE_URL")
    ENV = os.getenv("ENV", "Production")
    METHOD = os.getenv("METHOD", "20")