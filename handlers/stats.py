from aiogram import types, Router
from aiogram.filters import Command
import sqlite3
import matplotlib.pyplot as plt
from config import DB_PATH

router = Router()

@router.message(Command("stats"))
async def stats(message: types.Message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, h.price, h.date 
        FROM products p
        JOIN price_history h ON p.id = h.product_id
        WHERE p.user_id=? 
        ORDER BY h.date ASC
    """, (message.from_user.id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await message.answer("📊 There is no data for statistics.")
        return

    names = {}
    for name, price, date in rows:
        if name not in names:
            names[name] = {"dates": [], "prices": []}
        names[name]["dates"].append(date)
        names[name]["prices"].append(price)

    for name, data in names.items():
        plt.figure(figsize=(6, 4))
        plt.plot(data["dates"], data["prices"], marker="o")
        plt.title(f"Price dynamics: {name}")
        plt.xlabel("Date")
        plt.ylabel("Price, UAH")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("stats.png")
        plt.close()
        with open("stats.png", "rb") as photo:
            await message.answer_photo(photo)
