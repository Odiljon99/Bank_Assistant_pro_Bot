from aiogram import Router
from app.main_handlers import router as main_router
from app.handler.credit import router as credit_router

router = Router()
router.include_router(main_router)
router.include_router(credit_router)
