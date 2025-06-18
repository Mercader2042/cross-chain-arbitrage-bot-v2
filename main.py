import os, time, requests, schedule
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

PAIRS = ["STEEM", "TRX", "XLM", "DASH", "XNO", "XRP", "ATOM"]
MIN_MARGIN = 1.5  # porcentaje mínimo

def check_opportunities():
    try:
        # Aquí iría la lógica real de arbitraje cross-chain
        margin = 2.0  # ejemplo simulado
        if margin >= MIN_MARGIN:
            bot.send_message(chat_id=CHAT_ID,
                             text=f"📈 Oportunidad detectada: margen de {margin:.2f}%")
        print("[DEBUG] Comprobación realizada.")
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID,
                         text=f"⚠️ Error en check_opportunities:\n{e}")

schedule.every(30).minutes.do(lambda: bot.send_message(chat_id=CHAT_ID, text="✅ Ping debug"))
schedule.every(1).minutes.do(check_opportunities)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
