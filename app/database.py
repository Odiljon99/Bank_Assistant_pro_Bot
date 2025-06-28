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


# 🔍 Получить все записи (для администратора)
def get_all_users():
    cursor.execute("SELECT telegram_id, full_name, phone, birthday, pinfl FROM users")
    return cursor.fetchall()


# 🔍 Найти пользователя по ПИНФЛ или имени
def search_user_by_text(query: str):
    query = f"%{query.lower()}%"
    cursor.execute(
        "SELECT telegram_id, full_name, phone, birthday, pinfl FROM users WHERE LOWER(full_name) LIKE ? OR pinfl LIKE ?",
        (query, query)
    )
    return cursor.fetchall()


# 🔄 Обновить конкретное поле пользователя
def update_user_field(telegram_id: int, field: str, value: str):
    cursor.execute(f"UPDATE users SET {field} = ? WHERE telegram_id = ?", (value, telegram_id))
    conn.commit()


# 🔁 Получить пользователя по Telegram ID
def get_user_by_telegram_id(telegram_id: int):
    cursor.execute(
        "SELECT full_name, phone, birthday, pinfl FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    return cursor.fetchone()
