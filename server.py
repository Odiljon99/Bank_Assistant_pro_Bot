import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from app import bot, dp, config
from app.database import create_users_table  # ✅ добавили

# 👉 Импорт роутеров
from app.main_handlers import router as main_router
from app.handler.credit import router as credit_router

# 👉 Регистрация роутеров
dp.include_router(main_router)
dp.include_router(credit_router)

# ✅ При запуске
async def on_startup(app: web.Application):
    await create_users_table()  # ✅ создаём таблицу при старте
    webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен по адресу: {webhook_url}")

# ✅ При остановке
async def on_shutdown(app: web.Application):
    await bot.session.close()
    print("🛑 Сессия Telegram закрыта")

# Создание приложения aiohttp
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

setup_application(app, dp, bot=bot)
app.router.add_route("*", config.WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot))

# 🚀 Запуск
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
