import os
import json
import re
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MIN_PRICE = 900
MIN_DISCOUNT = 40

SEARCHES = [
    "https://www.prisjagt.dk/search?search=festool",
    "https://www.prisjagt.dk/search?search=makita"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124 Safari/537.36"
    )
}

HISTORY_FILE = "seen_products.json"


def send_telegram(text):

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


def load_seen():

    try:
        with open(HISTORY_FILE, "r") as f:
            return set(json.load(f))

    except Exception:
        return set()


def save_seen(data):

    with open(HISTORY_FILE, "w") as f:
        json.dump(list(data), f)


def interesting_product(title):

    title = title.lower()

    keep_words = [
        "festool",
        "systainer",
        "makita",
        "18v",
        "lxt",
        "xgt",
        "battery",
        "batteri"
    ]

    return any(word in title for word in keep_words)


def extract_price(text):

    matches = re.findall(r"(\d[\d\.\s]{2,8})\s*kr", text.lower())

    if not matches:
        return None

    try:
        value = matches[0]
        value = value.replace(".", "")
        value = value.replace(" ", "")
        return int(value)
    except:
        return None


def extract_discount(text):

    matches = re.findall(r"(\d{1,2})\s*%", text)

    if not matches:
        return None

    try:
        return int(matches[0])
    except:
        return None


seen = load_seen()
updated_seen = set(seen)

hits = 0

for url in SEARCHES:

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text_blocks = soup.find_all(
            ["a", "article", "div"]
        )

        for element in text_blocks:

            text = element.get_text(
                " ",
                strip=True
            )

            if len(text) < 20:
                continue

            if not interesting_product(text):
                continue

            price = extract_price(text)

            if not price:
                continue

            if price < MIN_PRICE:
                continue

            discount = extract_discount(text)

            if discount is None:
                continue

            if discount < MIN_DISCOUNT:
                continue

            product_id = text[:150]

            if product_id in seen:
                continue

            if discount >= 60:
                icon = "🚨🚨 RØVERKØB"
            elif discount >= 50:
                icon = "🔥 MEGET GODT TILBUD"
            else:
                icon = "🛠 TILBUD"

            send_telegram(
                f"""{icon}

{text[:400]}

Pris: {price} kr.
Rabat: {discount} %

{url}
"""
            )

            updated_seen.add(product_id)

            hits += 1

    except Exception as e:

        send_telegram(
            f"Fejl under scanning:\n{e}"
        )

save_seen(updated_seen)

send_telegram(
    f"✅ Scan afsluttet\nFundet: {hits} nye tilbud"
)
