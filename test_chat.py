import unittest
import sqlite3
from src.database import init_db, save_message, get_history, save_weather_history, get_weather_history, clear_history


class TestChatbot(unittest.TestCase):

    def setUp(self):
        # Inicializace testovací databáze a vyčištění
        self.conn = init_db()
        if self.conn is None:
            raise Exception("Nepodařilo se inicializovat databázi!")
        self.cursor = self.conn.cursor()
        clear_history()  # Vyčistí historii před každým testem

    def tearDown(self):
        # Vyčištění po testu
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def test_init_db(self):
        # Ověření, že tabulka byla vytvořena
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='messages';"
        )
        self.assertIsNotNone(self.cursor.fetchone())

    def test_add_message(self):
        # Přidání zprávy a ověření
        save_message("Verca", "Ahoj!")
        self.cursor.execute(
            "SELECT user_message, bot_message FROM messages WHERE user_message = 'Verca'"
        )
        result = self.cursor.fetchone()
        self.assertEqual(result, ("Verca", "Ahoj!"))

    def test_get_history(self):
        # Přidání dvou zpráv a kontrola historie
        save_message("Verca", "Ahoj!")
        save_message("Verca", "Jak se máš?")
        history = get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['uzivatel'], "Verca")
        self.assertEqual(history[0]['chatbot'], "Ahoj!")
        self.assertEqual(history[1]['uzivatel'], "Verca")
        self.assertEqual(history[1]['chatbot'], "Jak se máš?")

    def test_weather_history(self):
        # Test ukládání a načítání historie počasí
        save_weather_history("Praha", "Slunečno, 25°C")
        save_weather_history("Brno", "Deštivo, 18°C")
        history = get_weather_history()
        print("Historie počasí:", history)  # Přidáno pro ladění
        self.assertTrue("Praha: Slunečno, 25°C" in history)
        self.assertTrue("Brno: Deštivo, 18°C" in history)
        self.assertEqual(history.count(", "),
                         3)  # Očekáváme 3 čárky (2 v response + 1 oddělovač)

    def test_error_handling(self):
        # Test chování při neplatním vstupu
        save_message("", "")  # Prázdný vstup
        self.cursor.execute("SELECT user_message, bot_message FROM messages")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 1)  # Měl by se uložit i prázdný záznam


if __name__ == "__main__":
    unittest.main()
