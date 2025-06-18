import os
import requests
import time
import hmac
import hashlib
import base64
import json

from telegram import Bot

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# MEXC
API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")

def get_mexc_spot_balance():
    base_url = "https://api.mexc.com"
    endpoint = "/api/v3/account"
    url = base_url + endpoint

    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"

    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-MEXC-APIKEY": API_KEY
    }

    response = requests.get(f"{url}?{query_string}&signature={signature}", headers=headers)

    if response.status_code == 200:
        balances = response.json().get("balances", [])
        return balances
    else:
        return f"Error {response.status_code}: {response.text}"

# Ejecutamos al arrancar
result = get_mexc_spot_balance()

# Mandamos resultado a Telegram
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Resultado conexión MEXC:\n{result}")


