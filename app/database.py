import aiosqlite


async def create_users_table():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                full_name TEXT,
                phone TEXT,
                birthday TEXT,
                pinfl TEXT
            )
        """)
        await db.commit()


async def save_user(telegram_id, full_name, phone, birthday, pinfl):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (telegram_id, full_name, phone, birthday, pinfl)
            VALUES (?, ?, ?, ?, ?)
        """, (telegram_id, full_name, phone, birthday, pinfl))
        await db.commit()


async def get_user_by_telegram_id(telegram_id):
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "telegram_id": row[0],
                "full_name": row[1],
                "phone": row[2],
                "birthday": row[3],
                "pinfl": row[4]
            }
        return None


async def update_user_field(telegram_id, field, value):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(f"UPDATE users SET {field} = ? WHERE telegram_id = ?", (value, telegram_id))
        await db.commit()
