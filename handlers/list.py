from aiogram import types, Router
from aiogram.filters import Command
import sqlite3
from config import DB_PATH

router = Router()

@router.message(Command("list"))
async def list_products(message: types.Message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, url, last_price FROM products WHERE user_id=?", (message.from_user.id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await message.answer("📋 У тебе ще немає відстежуваних товарів.")
    else:
        msg = "📋 Список товарів:\n"
        for name, url, price in rows:
            msg += f"- {name}: {price or '---'} грн\n{url}\n"
        await message.answer(msg)
