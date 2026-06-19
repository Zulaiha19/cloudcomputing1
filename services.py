import requests
from config import Config

def get_prayer_times(city, country):
    """
    Fungsi untuk mengambil data jadwal sholat dari API Aladhan.
    """
    if not Config.BASE_URL:
        return {"error": "BASE_URL tidak ditemukan di konfigurasi"}

    url = f"{Config.BASE_URL}?city={city}&country={country}&method={Config.METHOD}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data["code"] != 200:
                return {"error": data["status"]}

            timings = data["data"]["timings"]

            return {
                "city": city.title(),
                "country": country.title(),
                "fajr": timings["Fajr"],
                "dhuhr": timings["Dhuhr"],
                "asr": timings["Asr"],
                "maghrib": timings["Maghrib"],
                "isha": timings["Isha"],
                "env": Config.ENV
            }

        return {"error": f"HTTP Error {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": "Gagal terhubung ke server API jadwal sholat."}
    except Exception as e:
        return {"error": str(e)}