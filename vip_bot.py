import os
from main import run
from data_collector import get_matches
from telegram import Bot
from config import TELEGRAM_CHAT_ID_VIP as CHAT_ID

TOKEN = os.getenv("TELEGRAM_TOKEN")


def format_msg(bet):
    return (
        f"🔥 VIP TIP 🔥\n\n"
        f"➡️ Mercado: {bet['type'].upper()}\n"
        f"📈 Probabilidade: {bet['prob']:.2%}\n"
        f"💰 Odds: {bet['odds']}\n"
        f"📊 EV: {bet['ev']:.2f}\n"
        f"⭐ Confiança: {bet['score']:.4f}"
    )


def main():
    matches = get_matches()
    _, vip = run(matches)

    bot = Bot(token=TOKEN)

    if not vip:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Mercado com baixa confiança hoje.")
        return

    bot.send_message(chat_id=CHAT_ID, text="🔥 MELHORES OPORTUNIDADES (VIP)\n")

    for bet in vip:
        bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))


if __name__ == "__main__":
    main()
