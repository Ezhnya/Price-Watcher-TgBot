import requests
from bs4 import BeautifulSoup

def get_price(url: str) -> float | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=7)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        selectors = ["p.product-price__big", "span.price", "div.product-price__top"]
        for sel in selectors:
            price_tag = soup.select_one(sel)
            if price_tag:
                price = "".join(ch for ch in price_tag.text if ch.isdigit())
                if price:
                    return float(price)
    except Exception as e:
        print("Parsing problem:", e)
    return None
