import logging
from aiogram import Bot, Dispatcher, executor
from config import TOKEN
from handlers import register_handlers
from scheduler import setup_scheduler
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Реєструємо хендлери
register_handlers(dp)

# Підключаємо планувальник
setup_scheduler(dp, bot)

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp, skip_updates=True)
