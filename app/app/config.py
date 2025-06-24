import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
