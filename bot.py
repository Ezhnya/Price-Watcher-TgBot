import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import init_db
from scheduler import setup_scheduler

from handlers.start import router as start_router
from handlers.add import router as add_router
from handlers.list import router as list_router
from handlers.remove import router as remove_router
from handlers.stats import router as stats_router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()


    dp.include_router(start_router)
    dp.include_router(add_router)
    dp.include_router(list_router)
    dp.include_router(remove_router)
    dp.include_router(stats_router)

    init_db()
    

    setup_scheduler(dp, bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
