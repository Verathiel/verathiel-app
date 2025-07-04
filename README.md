# 🤖 Verathiel – Interaktivní chatbot

Verathiel je chatbot napsaný v Pythonu (Flask), který umí reagovat na přirozený jazyk, přepínat mezi češtinou a angličtinou, pamatovat si konverzaci, zobrazit počasí nebo říct vtip. Projekt je responzivní, s přepínáním témat (světlý/tmavý režim) a použitím SQLite databáze.

---

## 🎯 Hlavní funkce

- 🗣️ Pozdravy a oslovení se zapamatováním jména
- 🌦️ Počasí pro zadané město (OpenWeatherMap API)
- 🇨🇿/🇬🇧 Přepínání jazyků (`Mluv česky` / `Speak English`)
- 📅 Datum a čas, emoce, osobnost, vtipy
- 💬 Ukládání historie konverzace a počasí (SQLite)

---

## 🧰 Použité technologie

- **Python**, **Flask**
- **HTML/CSS + JavaScript** (responsivní UI)
- **SQLite databáze**
- **unittest** pro testování
- **OpenWeatherMap API**

---

## 🔧 Lokální spuštění

```bash
git clone https://github.com/veronikaflachso/verathiel-app.git
cd verathiel-app

# Vytvoř soubor .env a přidej API klíč:
# API_KEY=tvuj_klic
# WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather

pip install -r requirements.txt
python chatbot.py
📦 Nebo spusť rovnou v Replitu:
👉 Verathiel na Replit

🧪 Testování
bash
Zkopírovat
Upravit
python test_chat.py
Testuje inicializaci databáze, ukládání zpráv, historii počasí a funkce chatbota.

🚀 Plány do budoucna
Vylepšené UI (grafické)

Kontextová paměť

Vlastní trénovaná reakční logika

👩‍💻 Autor
Veronika Flachsová
📧 veronikaflachsova186@gmail.com
🧠 Junior Python Developer & Tester
