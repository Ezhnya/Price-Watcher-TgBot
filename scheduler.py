from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parsers import get_price
import sqlite3
from config import DB_PATH

def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, name, url, last_price FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_price(product_id, new_price):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE products SET last_price=? WHERE id=?", (new_price, product_id))
    cur.execute("INSERT INTO price_history(product_id, price) VALUES (?, ?)", (product_id, new_price))
    conn.commit()
    conn.close()

async def check_prices(bot):
    products = get_all_products()
    for pid, user_id, name, url, last_price in products:
        new_price = get_price(url)
        if new_price is not None:
            if not last_price or new_price < last_price:
                await bot.send_message(
                    user_id,
                    f"📉 The price fell to {name}!\nBefore: {last_price or '---'} UAH\nAfter: {new_price} UAH"
                )
            update_price(pid, new_price)

def setup_scheduler(dp, bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_prices, "interval", minutes=60, args=[bot])
    scheduler.start()
