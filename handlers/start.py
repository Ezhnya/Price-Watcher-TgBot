from aiogram import types, Router
from aiogram.filters import Command
import sqlite3
from config import DB_PATH

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (message.from_user.id,))
    conn.commit()
    conn.close()
    await message.answer(
        "👋 Привіт! Я UA Price Watcher Bot.\n"
        "Додай товар для відстеження: /add <назва> <посилання>"
    )
