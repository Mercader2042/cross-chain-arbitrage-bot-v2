import os
import requests
import time
import hmac
import hashlib
from telegram import Bot

# Leer variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")

# Mostrar en logs si las variables están bien cargadas
print("TELEGRAM_TOKEN:", "OK" if TELEGRAM_TOKEN else "NO DEFINIDO")
print("TELEGRAM_CHAT_ID:", TELEGRAM_CHAT_ID)
print("MEXC_API_KEY:", API_KEY)
print("MEXC_API_SECRET existe:", bool(API_SECRET))

# Validar que están todas las variables
if not all([TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, API_KEY, API_SECRET]):
    raise ValueError("❌ Alguna variable de entorno no está definida correctamente.")

# Inicializar el bot
bot = Bot(token=TELEGRAM_TOKEN)

# Función para consultar saldo en MEXC
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

    try:
        response = requests.get(f"{url}?{query_string}&signature={signature}", headers=headers)
        if response.status_code == 200:
            balances = response.json().get("balances", [])
            return balances
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Exception during API call: {str(e)}"

# Ejecutar la función y enviar resultado a Telegram
result = get_mexc_spot_balance()
print("Resultado conexión MEXC:", result)  # <--- Esta línea es nueva
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Resultado conexión MEXC:\n{result}")
