import requests
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ENV = os.getenv("ENV")

def get_prayer_times(city, country):
    url = f"{BASE_URL}?city={city}&country={country}&method=11"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            timings = data["data"]["timings"]

            print("\n===== JADWAL SHOLAT =====")
            print(f"Kota       : {city}")
            print(f"Negara     : {country}")
            print(f"Subuh      : {timings['Fajr']}")
            print(f"Dzuhur     : {timings['Dhuhr']}")
            print(f"Ashar      : {timings['Asr']}")
            print(f"Maghrib    : {timings['Maghrib']}")
            print(f"Isya       : {timings['Isha']}")
            print(f"Environment: {ENV}")
            print("==========================\n")

        else:
            print("\n===== ERROR API =====")
            print("Status Code :", response.status_code)
            print("Pesan       :", response.text)
            print("=====================\n")

    except Exception as e:
        print("\n===== ERROR SYSTEM =====")
        print("Terjadi kesalahan:", e)
        print("========================\n")


if __name__ == "__main__":
    print("=== Aplikasi Jadwal Sholat ===")
    city = input("Masukkan nama kota: ")
    country = input("Masukkan negara: ")
    get_prayer_times(city, country)