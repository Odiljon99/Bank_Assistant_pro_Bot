import os
import logging
from flask import Flask, request, abort
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
ADMINS = os.getenv("ADMINS", "").split(",")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

app = Flask(__name__)
loop = asyncio.get_event_loop()

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = types.Update(**request.get_json())
        asyncio.run(dp.feed_update(bot, update))
        return "OK"
    else:
        abort(403)

@app.route("/", methods=["GET"])
def root():
    return "Webhook bot is running!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=10000)