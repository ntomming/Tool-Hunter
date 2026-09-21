import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SEARCH_TERMS = [
    "Festool",
    "Makita"
]


def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


for search_term in SEARCH_TERMS:

    message = f"""
🔎 Prisjagt søgning

Mærke:
{search_term}

Link:
https://www.prisjagt.dk/search?search={search_term}
"""

    send_telegram(message)

print("Done")
