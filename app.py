import requests
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Ambil konfigurasi dari .env
BASE_URL = os.getenv("BASE_URL")
ENV = os.getenv("ENV")
METHOD = os.getenv("METHOD", "20")


def get_prayer_times(city, country):
    # Cek apakah BASE_URL berhasil dibaca
    if not BASE_URL:
        print("\n===== ERROR =====")
        print("BASE_URL tidak ditemukan di file .env")
        print("=================\n")
        return

    # Susun URL API
    url = f"{BASE_URL}?city={city}&country={country}&method={METHOD}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Cek apakah API berhasil mengembalikan data
            if data["code"] != 200:
                print("\n===== ERROR API =====")
                print(data["status"])
                print("=====================\n")
                return

            timings = data["data"]["timings"]

            print("\n========== JADWAL SHOLAT ==========")
            print(f"Kota        : {city.title()}")
            print(f"Negara      : {country.title()}")
            print(f"Subuh       : {timings['Fajr']}")
            print(f"Dzuhur      : {timings['Dhuhr']}")
            print(f"Ashar       : {timings['Asr']}")
            print(f"Maghrib     : {timings['Maghrib']}")
            print(f"Isya        : {timings['Isha']}")
            print("-----------------------------------")
            print(f"Environment : {ENV}")
            print("===================================\n")

        else:
            print("\n===== ERROR API =====")
            print("Status Code :", response.status_code)
            print("Response    :", response.text)
            print("=====================\n")

    except requests.exceptions.RequestException as e:
        print("\n===== ERROR SYSTEM =====")
        print("Terjadi kesalahan:", e)
        print("========================\n")


if __name__ == "__main__":
    print("===================================")
    print("     APLIKASI JADWAL SHOLAT")
    print("===================================")

    city = input("Masukkan nama kota    : ")
    country = input("Masukkan nama negara  : ")

    get_prayer_times(city, country)