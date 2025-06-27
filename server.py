from flask import Flask, request
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio
from app import bot, dp
from app import config
from app.database import cursor, conn
from app.handlers import router
import os

dp.include_router(router)

async def on_startup():
    await bot.set_webhook(f"https://{os.getenv('RAILWAY_STATIC_URL')}{config.WEBHOOK_PATH}")

app = web.Application()
setup_application(app, dp, bot=bot)
app.router.add_route("*", config.WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot))

if __name__ == "__main__":
    asyncio.run(on_startup())
    web.run_app(app, host="0.0.0.0", port=10000)
