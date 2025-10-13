from aiogram import types, Router
from aiogram.filters import Command
import sqlite3
from config import DB_PATH
from parsers import get_price

router = Router()

@router.message(Command("add"))
async def add_product(message: types.Message):
    try:
        _, name, url = message.text.split(maxsplit=2)
    except ValueError:
        await message.answer("❌ Write like this: /add <Name> <Link>")
        return

    price = get_price(url)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO products(user_id, name, url, last_price) VALUES (?, ?, ?, ?)",
                (message.from_user.id, name, url, price))
    product_id = cur.lastrowid
    if price:
        cur.execute("INSERT INTO price_history(product_id, price) VALUES (?, ?)", (product_id, price))
    conn.commit()
    conn.close()

    await message.answer(f"✅ Added {name}\nCurrent price: {price or 'unknown'} UAH")
