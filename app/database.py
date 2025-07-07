✅ Обновлённый файл database.py с поддержкой языка

import aiosqlite

DB_NAME = "users.db"

📌 Создание таблицы

async def create_users_table(): async with aiosqlite.connect(DB_NAME) as db: await db.execute(''' CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER UNIQUE, full_name TEXT, phone TEXT, birthday TEXT, pinfl TEXT, lang TEXT DEFAULT 'ru' ) ''') await db.commit()

✅ Сохранить пользователя

async def save_user(telegram_id, full_name, phone, birthday, pinfl, lang="ru"): async with aiosqlite.connect(DB_NAME) as db: await db.execute( "INSERT OR REPLACE INTO users (telegram_id, full_name, phone, birthday, pinfl, lang) VALUES (?, ?, ?, ?, ?, ?)", (telegram_id, full_name, phone, birthday, pinfl, lang) ) await db.commit()

🔍 Получить по Telegram ID

async def get_user_by_telegram_id(telegram_id: int): async with aiosqlite.connect(DB_NAME) as db: async with db.execute("SELECT full_name, phone, birthday, pinfl, lang FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor: return await cursor.fetchone()

🔍 Все пользователи

async def get_all_users(): async with aiosqlite.connect(DB_NAME) as db: async with db.execute("SELECT telegram_id, full_name, phone, birthday, pinfl, lang FROM users") as cursor: return await cursor.fetchall()

🔍 Поиск по имени или ПИНФЛ

async def search_user_by_text(query: str): query = f"%{query.lower()}%" async with aiosqlite.connect(DB_NAME) as db: async with db.execute( "SELECT telegram_id, full_name, phone, birthday, pinfl, lang FROM users WHERE LOWER(full_name) LIKE ? OR pinfl LIKE ?", (query, query) ) as cursor: return await cursor.fetchall()

🔄 Обновить поле

async def update_user_field(telegram_id: int, field: str, value: str): async with aiosqlite.connect(DB_NAME) as db: await db.execute(f"UPDATE users SET {field} = ? WHERE telegram_id = ?", (value, telegram_id)) await db.commit()

✅ Обновить язык

async def update_user_language(telegram_id: int, lang: str): await update_user_field(telegram_id, "lang", lang)

🔍 Получить язык

async def get_user_language(telegram_id: int) -> str: async with aiosqlite.connect(DB_NAME) as db: async with db.execute("SELECT lang FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor: result = await cursor.fetchone() return result[0] if result else "ru"

                                                        
