Verathiel - Chatbot Project

Popis

Verathiel je interaktivní chatbot, který jsem vyvinula jako ukázku svých dovedností v programování. Projekt demonstruje moje schopnosti v HTML/CSS, JavaScriptu, Pythonu (Flask) a práci s databází SQLite. Chatbot je navržen s responsivním designem a dvěma tématy – světlým a tmavým.

Funkce Chatbota

Pozdravy a oslovení: Reaguje na pozdravy (např. "Ahoj", "Hello") a může oslovit uživatele podle jména, pokud je zadá (např. "Jmenuji se Kuba").
Počasí: Zobrazuje aktuální počasí pro zadané město (např. "Jaké je počasí v Praze?") s detaily jako teplota, vlhkost a rychlost větru.
Jazykové přepínání: Uživatelé mohou přepnout jazyk příkazy "Mluv česky" nebo "Speak English".
Emoce: Reaguje na pozitivní (např. "Jsem rád") i negativní emoce (např. "Jsem smutný") s náhodnými odpověďmi.
Historie konverzace: Ukládá a zobrazuje historii zpráv (příkaz "Zobraz historii" nebo "Show history").
Datum a čas: Poskytuje aktuální čas a datum (např. "Kolik je hodin?").
Koníčky a vtipy: Může mluvit o svých "koníčcích" (např. hvězdářství) nebo vyprávět vtipy (např. "Řekni vtip").
Osobní identita: Odpovídá na otázky typu "Kdo jsi?" s humornými nebo kreativními popisy.

Mé Dovednosti
Po několika měsících spolupráce a učení jsem si osvojila široké spektrum dovedností, které se odrážejí v tomto projektu:

Programování v Pythonu: Základy syntaxe, práce s knihovnami jako sqlite3, requests a unidecode, a tvorba funkčních skriptů.
UI Design: Navrhování jednoduchého a intuitivního textového rozhraní pro interakci s chatbotem, s ohledem na uživatelskou přívětivost.
Řešení problémů v kódech: Schopnost identifikovat a odstraňovat chyby (např. syntax errors, databázové konflikty) pomocí ladění a logování.
Práce s databázemi: Návrh a správa SQLite databáze pro ukládání zpráv a historie počasí, včetně optimalizace dotazů.
API integrace: Úspěšná integrace OpenWeatherMap API pro získávání a zpracování dat o počasí v reálném čase.
Testování softwaru: Vytvoření a provádění jednotkových testů pomocí unittest pro zajištění kvality kódu.
Verzování a spolupráce: Použití Git a GitHub pro správu kódu a přípravu na týmovou spolupráci.
Plánování a organizace: Strukturované přístupy k vývoji projektu, včetně rozdělení na moduly (např. src/database.py, src/weather.py).
Práce s daty: Manipulace s JSON a textovými daty pro jazykové překlady a ukládání uživatelských preferencí.

Instalace

Chceš projekt vyzkoušet lokálně? Postup je jednoduchý:





Naklonuj repozitář:

git clone https://github.com/veronikaflachso/verathiel-app.git



Nastav proměnné prostředí:





Vytvoř soubor .env v rootu a přidej API klíč pro OpenWeatherMap:

API_KEY=tvuj_api_klic
WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather



Nainstaluj závislosti (pokud ještě nejsou):

pip install requests



Spusť aplikaci:

python chatbot.py

Případně můžeš chatbot vyzkoušet přímo online na Replit, kde je již přednastavený!

Použití





Interakce probíhá přes textový vstup. Zkus například:





"Ahoj, jmenuji se Kuba"



"Jaké je počasí v Praze?"



"Mluv česky"



Historii zpráv zobrazíš příkazem "Zobraz historii".

Testování

Testy jsou implementovány pomocí unittest. Spusť je pro ověření funkčnosti:

python test_chat.py

Testy pokrývají inicializaci databáze, ukládání zpráv, historii konverzace a historii počasí.

Plány do budoucna

Rozšíření funkcí
Učení se z konverzací
Vylepšení uživatelského rozhraní s grafickým UI.

Autor

Veronika Flachsová
Kontakt: veronikaflachsova186@gmail.com

Licence

MIT Licence