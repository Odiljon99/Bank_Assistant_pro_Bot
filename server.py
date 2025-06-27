import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from app import bot, dp, config
from app.database import cursor, conn
from app.handlers import router

# Подключаем маршруты
dp.include_router(router)

# Функция, вызываемая при старте приложения
async def on_startup(app: web.Application):
    await bot.set_webhook(f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}")
    print("✅ Webhook установлен!")

# Создаем aiohttp-приложение
app = web.Application()
app.on_startup.append(on_startup)

# Настройка aiogram webhook
setup_application(app, dp, bot=bot)

# Добавляем маршрут webhook
app.router.add_route("*", config.WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot))

# Запуск приложения
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
