import logging
from dotenv import load_dotenv
import os

# Nastavení logování
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Načtení proměnných z .env souboru
load_dotenv()

# Načtení API klíče z proměnné prostředí
API_KEY = os.getenv("WEATHER_API_KEY")
logging.debug(f"Načtený API klíč: {API_KEY}")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
CITY_MAPPING = {
    "praze": "Praha",
    "brnu": "Brno",
    # další mapování
}
CITY_DECLENSION = {
    "Praha": "Praze",
    "Brno": "Brnu",
    # další skloňování
}
uzivatelske_info = {"language": "cs"}
prazdne_vstupy = 0
posledni_preference = None
posledni_zprava = None
