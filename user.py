import threading
import asyncio
import re
import requests
from flask import Flask, request
from telethon import TelegramClient, events

# ----------------------------------------
# CONFIG
# ----------------------------------------
API_ID = 25545982
API_HASH = "adf731033d9de2faafbbcdb2bfa519a9"
BOT_TOKEN = "7979757018:AAEj3Y-_Jc3iWLJWmcx86ZbqEhJYo0JFhrc"
GROUP_ID = -1002757804832
WEBHOOK_URL = "https://your-app.onrender.com/hook"
CARDXABAR_ID = 915326936

# ----------------------------------------
# TELETHON CLIENT
# ----------------------------------------
client = TelegramClient("userbot", API_ID, API_HASH)


@client.on(events.NewMessage(from_users=CARDXABAR_ID))
async def handler(event):
    text = event.raw_text

    summa_match = re.search(r"\+ ([\d\s\.,]+) UZS", text)
    card_match  = re.search(r"\*\*\*(\d{4})", text)

    if summa_match and card_match:
        summa_raw = summa_match.group(1)
        summa_clean = summa_raw.replace(" ", "").replace(",", "").split(".")[0]
        card = card_match.group(1)
        payload = f"PAYMENT|{summa_clean}|{card}"

        try:
            requests.post(WEBHOOK_URL, json={"data": payload})
        except:
            pass


# ----------------------------------------
# USERBOT THREAD ISHLATISH
# ----------------------------------------
def start_userbot():
    loop = asyncio.new_event_loop()          # yangi loop
    asyncio.set_event_loop(loop)             # loopni shu threadga biriktirish
    print("Userbot ishga tushdi!")

    loop.run_until_complete(client.start())  # start async
    loop.run_until_complete(client.run_until_disconnected())  # doimiy ishlaydi


# ----------------------------------------
# FLASK WEBHOOK
# ----------------------------------------
app = Flask(__name__)

@app.route("/hook", methods=["POST"])
def hook():
    data = request.json.get("data", None)
    if not data:
        return "no data", 400

    # EXACT xabar guruhga
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": GROUP_ID, "text": data}
    )
    return "ok", 200


@app.route("/")
def home():
    return "running", 200


def start_flask():
    print("Webhook server ishga tushdi!")
    app.run(host="0.0.0.0", port=10000)


# ----------------------------------------
# IKKALA XIZMATNI BIRGA ISHLATISH
# ----------------------------------------
if __name__ == "__main__":
    threading.Thread(target=start_userbot).start()
    threading.Thread(target=start_flask).start()