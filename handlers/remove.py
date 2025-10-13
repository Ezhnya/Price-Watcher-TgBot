from aiogram import types, Router
from aiogram.filters import Command
import sqlite3
from config import DB_PATH

router = Router()

@router.message(Command("remove"))
async def remove_product(message: types.Message):
    try:
        _, name = message.text.split(maxsplit=1)
    except ValueError:
        await message.answer("❌ Write like this: /remove <Name>")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE user_id=? AND name=?", (message.from_user.id, name))
    conn.commit()
    conn.close()

    await message.answer(f"🗑 Deleted {name}")
