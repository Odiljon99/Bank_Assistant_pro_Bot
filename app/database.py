import sqlite3

# Соединение с БД (если файла нет — создастся)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    full_name TEXT,
    phone TEXT,
    birthday TEXT,
    pinfl TEXT
)
''')
conn.commit()
