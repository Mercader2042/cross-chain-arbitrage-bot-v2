import os
import requests
import time
import hmac
import hashlib
from telegram import Bot

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Falta TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en las variables de entorno")

bot = Bot(token=TELEGRAM_TOKEN)

# MEXC
API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("Falta MEXC_API_KEY o MEXC_API_SECRET en las variables de entorno")

def get_mexc_spot_balance():
    print("API_KEY:", API_KEY)
print("API_SECRET exists:", bool(API_SECRET))

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

    try:
        response = requests.get(f"{url}?{query_string}&signature={signature}", headers=headers)
        if response.status_code == 200:
            balances = response.json().get("balances", [])
            return balances
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Exception during API call: {str(e)}"

# Ejecutamos al arrancar
result = get_mexc_spot_balance()

# Mandamos resultado a Telegram
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Resultado conexión MEXC:\n{result}")
