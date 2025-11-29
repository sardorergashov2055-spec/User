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

WEBHOOK_URL = "https://user-wve8.onrender.com/hook"
CARDXABAR_ID = 5894219175      # @CardXabarBot TO‘G‘RI ID

# ----------------------------------------
# TELETHON USERBOT (SESSION REQUIRED)
# ----------------------------------------
client = TelegramClient("userbot", API_ID, API_HASH)

@client.on(events.NewMessage(from_users=CARDXABAR_ID))
async def handler(event):
    text = event.raw_text

    # SUMMA = + 4 950 000.00 UZS
    summa_match = re.search(r"\+ ([\d\s\.,]+) UZS", text)
    # CARD = ***4308
    card_match = re.search(r"\*\*\*(\d{4})", text)

    if not summa_match or not card_match:
        return

    summa_raw = summa_match.group(1)
    summa_clean = summa_raw.replace(" ", "").replace(",", "").split(".")[0]
    card = card_match.group(1)

    payload = f"PAYMENT|{summa_clean}|{card}"

    print("➡️ Webhookga yuborilmoqda:", WEBHOOK_URL, " | Data:", payload)

    try:
        res = requests.post(WEBHOOK_URL, json={"data": payload}, timeout=3)
        print("⬅️ Webhook javobi:", res.status_code)
    except Exception as e:
        print("❌ Webhook xato:", e)


# ----------------------------------------
# USERBOT THREAD
# ----------------------------------------
def start_userbot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("Userbot ishga tushdi!")

    async def runner():
        await client.start()
        await client.run_until_disconnected()

    loop.run_until_complete(runner())


# ----------------------------------------
# UNIVERSAL WEBHOOK (400 BO‘LMAYDI)
# ----------------------------------------
app = Flask(__name__)

@app.route("/hook", methods=["POST"])
def hook():

    raw = request.data.decode(errors="ignore")
    js = None

    try:
        js = request.get_json(silent=True)
    except:
        js = None

    print("📥 RAW:", raw)
    print("📥 JSON:", js)

    data = None

    # JSON format bo‘lsa
    if js and "data" in js:
        data = js["data"]

    # Agar oddiy text kelgan bo‘lsa
    if not data and raw:
        data = raw

    if not data:
        print("⚠️ HECH NIMA TOPILMADI, O‘TKAZILDI")
        return "ok", 200  # 400 EMAS

    # Guruhga yuborish
    try:
        requests.post(
            f"https://api.telegram.org/bot{ BOT_TOKEN }/sendMessage",
            json={"chat_id": GROUP_ID, "text": data}
        )
        print("📤 Guruhga yuborildi:", data)
    except Exception as e:
        print("❌ Guruhga yuborishda xato:", e)

    return "ok", 200



@app.route("/")
def home():
    return "running", 200


def start_flask():
    print("Webhook server ishga tushdi!")
    app.run(host="0.0.0.0", port=8080)


# ----------------------------------------
# START BOTH
# ----------------------------------------
if __name__ == "__main__":
    threading.Thread(target=start_userbot).start()
    threading.Thread(target=start_flask).start()
