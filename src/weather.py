import requests
from typing import Optional
import logging

# Nastavení logování
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from src.config import API_KEY, WEATHER_API_URL, CITY_MAPPING, CITY_DECLENSION, uzivatelske_info

# Slovník pro překlad popisů počasí
WEATHER_TRANSLATIONS = {
    "clear sky": "jasná obloha",
    "few clouds": "částečně oblačno",
    "scattered clouds": "roztroušená oblačnost",
    "broken clouds": "polopřehledná oblačnost",
    "overcast clouds": "zataženo",
    "shower rain": "přeháňky",
    "rain": "déšť",
    "thunderstorm": "bouřka",
    "snow": "sníh",
    "mist": "mlha",
    # Přidej další překlady podle potřeby
}


def get_weather(city: str) -> str:
    """
    Získá informace o počasí pro dané město z OpenWeatherMap API.

    Args:
        city (str): Název města.

    Returns:
        str: Popis počasí nebo chybová zpráva.
    """
    # Kontrola, zda je API klíč nastaven
    if not API_KEY:
        logging.error("API klíč není nastaven v proměnných prostředí.")
        return "Chyba: API klíč není nastaven."

    # Normalizace názvu města
    city_normalized = city.lower().strip()

    # Mapování sklonovaných tvarů měst na názvy pro API
    city_for_api = CITY_MAPPING.get(city_normalized,
                                    city_normalized.capitalize())

    # Sestavení URL pro API požadavek
    params = {
        "q": city_for_api,
        "appid": API_KEY,
        "units": "metric",
        "lang": uzivatelske_info.get("language", "cs")
    }
    url = f"{WEATHER_API_URL}?q={city_for_api}&appid={API_KEY}&units=metric&lang={uzivatelske_info.get('language', 'cs')}"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Vyvolá výjimku pro HTTP chyby
        data = response.json()

        if data.get("cod") != 200:
            logging.error(
                f"Chyba při získávání počasí pro {city_for_api}: {data.get('message')}"
            )
            return f"Nemohu najít počasí pro {city}. Zkus jiný název města!"

        # Získání dat o počasí
        temperature = data["main"]["temp"]
        description_en = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Překlad popisu počasí do češtiny
        description_cs = WEATHER_TRANSLATIONS.get(description_en,
                                                  description_en)

        # Sklonování názvu města pro výstup
        city_display = CITY_DECLENSION.get(city_for_api, city_for_api)

        # Sestavení odpovědi
        return f"Počasí v {city_display}: {description_cs}, teplota {temperature}°C, vlhkost {humidity}%, vítr {wind_speed} m/s."

    except requests.exceptions.RequestException as e:
        logging.error(f"Chyba při volání OpenWeatherMap API: {e}")
        return "Nepodařilo se získat počasí. Zkus to znovu později!"
