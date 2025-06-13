import random
import re
import logging
import json
import os
from datetime import datetime
from unidecode import unidecode

# Nastavení logování
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from src.config import uzivatelske_info, prazdne_vstupy, posledni_preference, posledni_zprava

# Načtení nebo aktualizace uživatelských dat po importu
DATA_FILE = os.path.join(os.path.dirname(__file__), "static", "user_data.json")
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        uzivatelske_info.update(json.load(f))  # Aktualizuje existující data
else:
    uzivatelske_info.setdefault("language",
                                "cs")  # Výchozí jazyk, pokud není nastaven


def save_user_data():
    """Uloží uživatelské informace do JSON souboru."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(uzivatelske_info, f, ensure_ascii=False, indent=4)


from src.weather import get_weather
from src.database import save_message, get_weather_history

# Načtení jazykových dat
with open(os.path.join(os.path.dirname(__file__), "static", "languages.json"),
          "r",
          encoding="utf-8") as f:
    lang_data = json.load(f)


def odpovedet(zprava):
    global prazdne_vstupy, posledni_preference, posledni_zprava
    # Normalizace zprávy na začátku (bez diakritiky)
    zprava_normalized = zprava.lower().strip()
    zprava_normalized_no_diacritics = unidecode(zprava_normalized)
    logging.debug(
        f"Zpráva: '{zprava_normalized}' (bez diakritiky: '{zprava_normalized_no_diacritics}')"
    )
    posledni_zprava = zprava_normalized

    # Prázdný vstup
    if not zprava_normalized:
        prazdne_vstupy += 1
        odpoved = (
            lang_data["responses"]["default"][uzivatelske_info["language"]][0]
            + " " + ("Are you there? Write something to continue!"
                     if uzivatelske_info["language"] == "en" else
                     "Hej, jsi tam ještě? Napiš něco, ať pokračujeme!")
        ) if prazdne_vstupy >= 3 else lang_data["responses"]["default"][
            uzivatelske_info["language"]][1]
    else:
        prazdne_vstupy = 0

        # Uložení jména
        if jmeno_match := re.search(
                r"jmenuji se (\w+)",
                zprava_normalized_no_diacritics) or re.search(
                    r"my name is (\w+)", zprava_normalized_no_diacritics):
            uzivatelske_info["jmeno"] = jmeno_match.group(1).capitalize()
            save_user_data()  # Ulož jméno po jeho nastavení
            odpoved = (
                f"Pěkně, {uzivatelske_info['jmeno']}! Rád tě poznávám. Jak ti můžu pomoci?"
                if uzivatelske_info["language"] == "cs" else
                f"Nice, {uzivatelske_info['jmeno']}! Glad to meet you. How can I help you?"
            )

        # Přepínání jazyka
        elif "speak english" in zprava_normalized_no_diacritics:
            uzivatelske_info["language"] = "en"
            save_user_data()  # Ulož jazyk po přepnutí
            odpoved = lang_data["responses"]["default"]["en"][
                0] + " Language switched to English!"
        elif "mluv cesky" in zprava_normalized_no_diacritics:
            uzivatelske_info["language"] = "cs"
            save_user_data()  # Ulož jazyk po přepnutí
            odpoved = lang_data["responses"]["default"]["cs"][
                0] + " Jazyk přepnut na češtinu!"

        # Zobrazení historie
        elif "zobraz historii" in zprava_normalized_no_diacritics or "show history" in zprava_normalized_no_diacritics:
            history = get_weather_history()
            odpoved = lang_data["responses"]["history"][
                uzivatelske_info["language"]][0].format(history=history)

        # Pozdrav s možným oslovením
        elif any(pozdrav in zprava_normalized_no_diacritics for pozdrav in
                 ["dobry den", "ahoj", "cau", "zdar", "hello", "hi"]):
            odpoved = (f"Ahoj, {uzivatelske_info.get('jmeno', 'příteli')}!"
                       if uzivatelske_info["language"] == "cs" else
                       f"Hello, {uzivatelske_info.get('jmeno', 'friend')}!"
                       ) + " " + random.choice(lang_data["responses"]["ahoj"][
                           uzivatelske_info["language"]])

        # Jak se máš?
        elif any(otazka in zprava_normalized_no_diacritics
                 for otazka in ["jak se mas", "jak se máš", "how are you"]):
            odpoved = random.choice(lang_data["responses"]["jak_se_mas"][
                uzivatelske_info["language"]])

        # Počasí - město + země
        elif weather_with_country_match := (
                re.search(r"jake je pocasi v (\w+)[, ]+(\w{2})",
                          zprava_normalized_no_diacritics)
                or re.search(r"what is the weather in (\w+)[, ]+(\w{2})",
                             zprava_normalized_no_diacritics)):
            city = weather_with_country_match.group(1).capitalize()
            country = weather_with_country_match.group(2).upper()
            logging.debug(
                f"Rozpoznána otázka na počasí pro město: {city}, země: {country}"
            )
            odpoved = get_weather(city=city)

        # Počasí - jen město
        elif weather_match := (re.search(r"jake je pocasi v (\w+)",
                                         zprava_normalized_no_diacritics)
                               or re.search(r"jaky je pocasi v (\w+)",
                                            zprava_normalized_no_diacritics)
                               or re.search(r"what is the weather in (\w+)",
                                            zprava_normalized_no_diacritics)):
            city = weather_match.group(1).capitalize()
            logging.debug(
                f"Rozpoznána otázka na počasí pro město: {city}, bez země")
            odpoved = get_weather(city=city)

        # Obecná otázka na počasí
        elif any(otazka in zprava_normalized_no_diacritics for otazka in [
                "jake je pocasi", "jaky je pocasi", "jak je venku",
                "jaky je venku", "what is the weather", "how is the weather"
        ]):
            logging.debug(
                "Rozpoznána obecná otázka na počasí, použit výchozí město Praha"
            )
            odpoved = get_weather()

        # Datum a čas
        elif any(otazka in zprava_normalized_no_diacritics for otazka in [
                "jaky je den", "kolik je hodin", "jaky je cas",
                "what day is it", "what time is it"
        ]):
            cas = datetime.now().strftime('%H:%M')
            den = datetime.now().strftime('%d. %m. %Y (%A)')
            odpoved = (f"Teď je {cas} hodin a dnešek je {den}."
                       if uzivatelske_info["language"] == "cs" else
                       f"It's {cas} and today is {den}.")

        # Emoce negativní
        elif any(e in zprava_normalized_no_diacritics for e in [
                "jsem smutny", "jsem smutna", "jsem zklamany", "jsem zklamana",
                "je mi smutno", "je mi zle", "neni mi dobre", "i am sad",
                "i am upset"
        ]):
            odpoved = (
                f"{random.choice(lang_data['responses']['emoce_negative'][uzivatelske_info['language']])}"
                + (f", {uzivatelske_info.get('jmeno', 'příteli')}."
                   if uzivatelske_info["language"] == "cs" else
                   f", {uzivatelske_info.get('jmeno', 'friend')}.")
            ) if uzivatelske_info.get("jmeno") else random.choice(
                lang_data["responses"]["emoce_negative"][
                    uzivatelske_info["language"]])

        # Emoce pozitivní
        elif any(e in zprava_normalized_no_diacritics for e in [
                "jsem rad", "jsem rada", "jsem vesely", "jsem vesela",
                "je mi dobre", "je mi super", "je mi fajn", "jsem stastny",
                "jsem stastna", "i am happy", "i am glad"
        ]):
            odpoved = (
                f"{random.choice(lang_data['responses']['emoce_positive'][uzivatelske_info['language']])}"
                + (f", {uzivatelske_info.get('jmeno', 'příteli')}!"
                   if uzivatelske_info["language"] == "cs" else
                   f", {uzivatelske_info.get('jmeno', 'friend')}!")
            ) if uzivatelske_info.get("jmeno") else random.choice(
                lang_data["responses"]["emoce_positive"][
                    uzivatelske_info["language"]])

        # Co děláš?
        elif any(otazka in zprava_normalized_no_diacritics for otazka in [
                "co delas", "co ted", "jak je", "jak se mas", "co děláš",
                "co teď děláš", "what are you doing"
        ]):
            aktivity_cs = [
                "přemýšlím o hvězdách nad tvou hlavou",
                "letím mezi světluškami", "sleduji tvoje myšlenky",
                "nechceš slyšet vtip?",
                "ještě toho moc neumím, ale co třeba nějaký počasí?"
            ]
            aktivity_en = [
                "thinking about stars above you", "flying with fireflies",
                "watching your thoughts", "preparing a magic joke"
            ]
            vybrane_aktivity = aktivity_cs if uzivatelske_info[
                "language"] == "cs" else aktivity_en
            odpoved = (
                f"Právě {random.choice(vybrane_aktivity)}. A ty co děláš, {uzivatelske_info.get('jmeno', 'příteli')}?"
                if uzivatelske_info["language"] == "cs" else
                f"Just {random.choice(vybrane_aktivity)}. And you, {uzivatelske_info.get('jmeno', 'friend')}, what are you doing?"
            )

        # Co umíš?
        elif any(otazka in zprava_normalized_no_diacritics for otazka in
                 ["co umis", "co umíš", "co víš", "what can you do"]):
            umeni_cs = [
                "odpovídat na otázky o počasí", "vyprávět vtipy", "říct čas",
                "mluvit o knihách a koníčcích", "říct ti co dělám",
                "zapamatuji si tvé jméno",
                "přepínat mezi světlým a tmavým režimem",
                "zeptej se kdo jsem...",
                "umím mluvit anglicky nebo se mrknem na naši historii v konverzaci"
            ]
            umeni_en = [
                "answer weather questions", "tell jokes", "tell the time",
                "talk about books and hobbies", "switch between light and dark"
            ]
            vybrane_umeni = umeni_cs if uzivatelske_info[
                "language"] == "cs" else umeni_en
            odpoved = (
                f"Umím {', '.join(vybrane_umeni[:-1])} a {vybrane_umeni[-1]}! Chceš vyzkoušet něco z toho, {uzivatelske_info.get('jmeno', 'příteli')}?"
                if uzivatelske_info["language"] == "cs" else
                f"I can {', '.join(vybrane_umeni[:-1])} and {vybrane_umeni[-1]}! Want to try something, {uzivatelske_info.get('jmeno', 'friend')}?"
            )

        # Knihy a koníčky
        elif any(otazka in zprava_normalized_no_diacritics for otazka in [
                "co ctes", "co čteš", "jake knihy", "jaké knihy",
                "jaky mas konicky", "jaké máš koníčky", "what do you read",
                "what are your hobbies"
        ]):
            jmeno = uzivatelske_info.get(
                'jmeno', 'příteli'
                if uzivatelske_info["language"] == "cs" else 'friend')
            knihy_konicky_cs = [
                f"Rád čtu sci-fi, co třeba Duny! A ty, jaké knížky máš rád/a, {jmeno}?",
                f"Mám rád/a dobrodružství, co třeba Pán prstenů. A ty, {jmeno}?",
                f"Mezi mými koníčky je hvězdářství. A co ty, {jmeno}?"
            ]
            knihy_konicky_en = [
                f"I enjoy sci-fi, like Dune! What about you, what books do you like, {jmeno}?",
                f"I like adventure stories, like Lord of the Rings. And you, {jmeno}?",
                f"One of my hobbies is stargazing. What about you, {jmeno}?"
            ]
            vybrane_knihy_konicky = knihy_konicky_cs if uzivatelske_info[
                "language"] == "cs" else knihy_konicky_en
            odpoved = random.choice(vybrane_knihy_konicky)

        # Kdo jsi?
        elif any(otazka in zprava_normalized_no_diacritics for otazka in [
                "kdo jsi", "co jsi zac", "jak se jmenujes",
                "jake je tve jmeno", "who are you"
        ]):
            popisy_cs = [
                "jsem Verathiel, strážce hvězdného prachu...a taky beta verze.",
                "Hádej...to byl vtip haha. Jsem chatbot",
                "Jsem tvůj digitální společník", "Nejsem nikdo, jen chatbot"
            ]
            popisy_en = [
                "I am Verathiel, guardian of stardust",
                "Guess... that was a joke haha. I am a chatbot",
                "your digital companion", "I am nobody, just a chatbot"
            ]
            vybrane_popisy = popisy_cs if uzivatelske_info[
                "language"] == "cs" else popisy_en
            odpoved = (
                f"{random.choice(vybrane_popisy)}. Rád ti pomůžu nebo tě pobavím, {uzivatelske_info.get('jmeno', 'příteli')}!"
                if uzivatelske_info["language"] == "cs" else
                f"{random.choice(vybrane_popisy)}. Glad to help or entertain you, {uzivatelske_info.get('jmeno', 'friend')}!"
            )

        # Vtip
        elif any(vtip in zprava_normalized_no_diacritics for vtip in [
                "vtip", "neco vtipneho", "zasmat", "joke", "something funny",
                "make me laugh"
        ]):
            odpoved = random.choice(
                lang_data["responses"]["vtip"][uzivatelske_info["language"]])

        # Fallback odpověď
        elif len(zprava_normalized.split()) >= 2:
            odpoved = random.choice(lang_data["responses"]["default"][uzivatelske_info["language"]]) + " " + \
                      ("What do you think?" if uzivatelske_info["language"] == "en" else "Co myslíš ty?") + \
                      (f", {uzivatelske_info.get('jmeno', '')}." if uzivatelske_info.get("jmeno") else "")

        # Základní fallback pro velmi krátkou zprávu
        else:
            odpoved = random.choice(lang_data["responses"]["default"][
                uzivatelske_info["language"]])

    # Uložení zprávy pouze jednou na konci
    if posledni_zprava and not any(zprava_normalized in z
                                   for z in [posledni_zprava, zprava]):
        save_message(zprava_normalized, odpoved)
    return odpoved
