import sqlite3
import logging
from datetime import datetime

# Nastavení logování
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def init_db():
    """
    Inicializuje databázi, pokud neexistuje, s tabulkami pro zprávy a historii počasí.
    Vrátí připojení k databázi.
    """
    conn = sqlite3.connect('data/chat_history.db')
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_message TEXT,
                      bot_message TEXT,
                      timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS weather_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      city TEXT,
                      response TEXT,
                      timestamp TEXT)''')
        conn.commit()
        logging.info("Databáze byla úspěšně inicializována.")
        return conn
    except Exception as e:
        logging.error(f"Chyba při inicializaci databáze: {e}")
        conn.close()
        return None


def save_message(user_message, bot_message):
    """
    Uloží zprávu uživatele a odpověď bota do databáze s aktuálním časovým razítkem.

    Args:
        user_message (str): Zpráva od uživatele.
        bot_message (str): Odpověď bota.
    """
    try:
        with sqlite3.connect('data/chat_history.db') as conn:
            c = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute(
                "INSERT INTO messages (user_message, bot_message, timestamp) VALUES (?, ?, ?)",
                (user_message, bot_message, timestamp))
            conn.commit()
            logging.debug(
                f"Uložena zpráva: {user_message}, odpověď: {bot_message}")
    except Exception as e:
        logging.error(f"Chyba při ukládání zprávy: {e}")


def save_weather_history(city, response):
    """
    Uloží historii požadavku na počasí do databáze s aktuálním časovým razítkem.

    Args:
        city (str): Název města.
        response (str): Odpověď s informací o počasí.
    """
    try:
        with sqlite3.connect('data/chat_history.db') as conn:
            c = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute(
                "INSERT INTO weather_history (city, response, timestamp) VALUES (?, ?, ?)",
                (city, response, timestamp))
            conn.commit()
            logging.debug(f"Uložena historie počasí pro město: {city}")
    except Exception as e:
        logging.error(f"Chyba při ukládání historie počasí: {e}")


def get_history():
    """
    Vrátí historii konverzací seřazenou podle času vzestupně.

    Returns:
        list: Seznam slovníků s klíči 'uzivatel', 'chatbot', 'timestamp'.
    """
    try:
        with sqlite3.connect('data/chat_history.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT user_message, bot_message, timestamp FROM messages ORDER BY timestamp ASC"
            )
            return [
                {
                    'uzivatel': row[0],  # Původní user_message
                    'chatbot': row[1],
                    'timestamp': row[2]
                } for row in c.fetchall()
            ]
    except Exception as e:
        logging.error(f"Chyba při načítání historie: {e}")
        return []


def get_weather_history():
    """
    Vrátí posledních 5 záznamů historie počasí seřazených podle času sestupně.

    Returns:
        str: Textový řetězec s historií nebo zpráva "Žádná historie", pokud je prázdná.
    """
    try:
        with sqlite3.connect('data/chat_history.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT city, response, timestamp FROM weather_history ORDER BY timestamp DESC LIMIT 5"
            )
            history_list = []
            for row in c.fetchall():
                history_list.append(f"{row[0]}: {row[1]} ({row[2]})")
            return ", ".join(
                history_list) if history_list else "Žádná historie."
    except Exception as e:
        logging.error(f"Chyba při načítání historie počasí: {e}")
        return "Žádná historie."


def clear_history():
    """
    Vymaže všechny záznamy z tabulek messages a weather_history.
    """
    try:
        with sqlite3.connect('data/chat_history.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM messages")
            c.execute("DELETE FROM weather_history")
            conn.commit()
            logging.info("Historie byla úspěšně vymazána.")
    except Exception as e:
        logging.error(f"Chyba při mazání historie: {e}")
