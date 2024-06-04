# database_setup.py
import sqlite3

def create_database():
    conn = sqlite3.connect('virtual_assistant.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_output TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()