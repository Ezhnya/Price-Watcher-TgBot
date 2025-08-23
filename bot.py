from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
from handlers import register_handlers
from database import init_db
from scheduler import setup_scheduler

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    setup_scheduler(dp, bot)
    init_db()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
