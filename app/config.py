import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Основные переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# ID админов — список чисел (можно указать свои ID)
ADMINS = [123456789]
