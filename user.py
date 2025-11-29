import threading
import asyncio
import re
import requests
from flask import Flask, request
from telethon import TelegramClient, events

# ==========================
# CONFIG
# ==========================
API_ID = 25545982
API_HASH = "adf731033d9de2faafbbcdb2bfa519a9"

BOT_TOKEN = "7979757018:AAEj3Y-_Jc3iWLJWmcx86ZbqEhJYo0JFhrc"
GROUP_ID = -1002757804832

WEBHOOK_URL = "https://user-wve8.onrender.com/hook"
CARDXABAR_ID = 5894219175   # TO‘G‘RI @CardXabarBot ID !!!

# ==========================
# TELETHON USERBOT
# ==========================
client = TelegramClient("userbot", API_ID, API_HASH)


@client.on(events.NewMessage(from_users=CARDXABAR_ID))
async def handler(event):
    text = event.raw_text

    summa_match = re.search(r"\+ ([\d\s\.,]+) UZS", text)
    card_match  = re.search(r"\*\*\*(\d{4})", text)

    if not summa_match or not card_match:
        return

    summa_raw = summa_match.group(1)
    summa_clean = summa_raw.replace(" ", "").replace(",", "").split(".")[0]
    card = card_match.group(1)

    payload = f"PAYMENT|{summa_clean}|{card}"

    print("➡️ Yuborilyapti →", WEBHOOK_URL, " | DATA:", payload)

    try:
        res = requests.post(WEBHOOK_URL, json={"data": payload}, timeout=5)
        print("⬅️ Webhook javobi:", res.status_code)
    except Exception as e:
        print("❌ Webhook xato:", e)


# ==========================
# USERBOT THREAD
# ==========================
def start_userbot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("Userbot ishga tushdi!")

    async def runner():
        await client.start()
        await client.run_until_disconnected()

    loop.run_until_complete(runner())


# ==========================
# UNIVERSAL WEBHOOK (NO 400 ERROR)
# ==========================
app = Flask(__name__)

@app.route("/hook", methods=["POST"])
def hook():

    raw = request.data.decode(errors="ignore")
    js = request.get_json(silent=True)

    print("📥 RAW:", raw)
    print("📥 JSON:", js)

    data = None

    # USERBOT yuboradigan format:
    if js and "data" in js:
        data = js["data"]

    # Telegram BOT xabari:
    if js and "message" in js and "text" in js["message"]:
        data = js["message"]["text"]

    # Telegram BOT status o‘zgarishi:
    if js and "my_chat_member" in js:
        new_status = js["my_chat_member"]["new_chat_member"]["status"]
        data = f"BOT STATUS: {new_status}"

    # Agar baribir topilmasa:
    if not data and raw:
        data = raw

    if not data:
        print("⚠️ DATA yo‘q, lekin 200 qaytaryapmiz (webhook o‘lmaydi)")
        return "ok", 200

    print("📤 Guruhga yuborilmoqda:", data)

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": GROUP_ID, "text": data}
        )
    except Exception as e:
        print("❌ Guruhga yuborish xatosi:", e)

    return "ok", 200


@app.route("/")
def home():
    return "running", 200


# ==========================
# FLASK THREAD
# ==========================
def start_flask():
    print("Webhook server ishga tushdi!")
    app.run(host="0.0.0.0", port=8080)


# ==========================
# START BOTH THREADS
# ==========================
if __name__ == "__main__":
    threading.Thread(target=start_userbot).start()
    threading.Thread(target=start_flask).start()
