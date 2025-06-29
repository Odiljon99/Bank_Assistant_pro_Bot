import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from app import bot, dp, config
from app.database import cursor, conn
from app.handler import router

# Подключаем маршруты
dp.include_router(router)

# ✅ Функция при запуске
async def on_startup(app: web.Application):
    webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен по адресу: {webhook_url}")

# ✅ Функция при остановке
async def on_shutdown(app: web.Application):
    await bot.session.close()
    print("🛑 Сессия Telegram закрыта")

# Создаём aiohttp-приложение
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)  # ← ВАЖНО: добавляем

# Настройка webhook
setup_application(app, dp, bot=bot)

# Добавляем маршрут webhook
app.router.add_route("*", config.WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot))

# Запуск
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
