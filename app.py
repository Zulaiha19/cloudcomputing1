import os
from dotenv import load_dotenv
from google import genai

from flask import Flask, render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, PrayerLog
from datetime import date, timedelta

# ======================
# ENV
# ======================
load_dotenv()

# ======================
# GEMINI
# ======================
# Inisialisasi client Google GenAI
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ======================
# FLASK APP
# ======================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sholatpro.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ======================
# AI ANALYSIS
# ======================
def get_ai_analysis(logs):
    """Fungsi untuk mendapatkan motivasi islami dari Gemini API."""
    prompt = f"""
Riwayat sholat user:
{logs}

Berikan motivasi islami singkat yang menyejukkan hati (max 150 kata).
"""

    try:
        # Menggunakan model gemini-2.0-flash (atau sesuai versi yang tersedia di akun Anda)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Maaf, asisten spiritual sedang beristirahat. ({str(e)})"

# ======================
# HOME
# ======================
@app.route("/", methods=["GET"])
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if not user:
        session.clear()
        return redirect("/login")

    # Generate range 7 hari terakhir
    days = [
        date.today() - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    selected_date = date.fromisoformat(
        request.args.get("date", str(date.today()))
    )

    log = PrayerLog.query.filter_by(
        user_id=user.id,
        date=selected_date
    ).first()

    ai_text = ""
    if user.subscription_type == "Premium":
        # Kirim data log untuk dianalisa
        log_data = str(log.__dict__) if log else "Belum ada data"
        ai_text = get_ai_analysis(log_data)

    return render_template(
        "index.html",
        user=user,
        days=days,
        selected_date=selected_date,
        log=log,
        ai_analysis=ai_text
    )

# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session["user_id"] = user.id
            return redirect("/")
        else:
            flash("Email atau password salah")

    return render_template("login.html")

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar")
            return redirect("/register")

        user = User(
            email=email,
            password=generate_password_hash(password),
            subscription_type="Gratis"
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ======================
# UPDATE PRAYER (AJAX)
# ======================
@app.route("/update_prayer", methods=["POST"])
def update_prayer():
    if "user_id" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()

    # Cari log berdasarkan tanggal yang dikirim dari frontend
    log = PrayerLog.query.filter_by(
        user_id=session["user_id"],
        date=data["date"]
    ).first()

    if not log:
        log = PrayerLog(
            user_id=session["user_id"],
            date=data["date"]
        )
        db.session.add(log)

    # Update status sholat (fajr, dhuhr, asr, maghrib, isha)
    setattr(log, data["prayer"], data["status"])

    db.session.commit()

    return jsonify({
        "success": True
    })

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)