import os
import time
from telegram import Bot

# Leer variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise Exception("Las variables de entorno TELEGRAM_TOKEN o TELEGRAM_CHAT_ID no están definidas")

# Crear bot
bot = Bot(token=TELEGRAM_TOKEN)

# Enviar mensaje de inicio para test
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Bot iniciado y funcionando correctamente!")

# Mantener el bot activo (ejemplo simple)
while True:
    # Aquí puedes poner la lógica del bot o esperar
    time.sleep(60)

