import os
from main import run
from telegram import Bot
from config import TELEGRAM_CHAT_ID_VIP as CHAT_ID

TOKEN = os.getenv("TELEGRAM_TOKEN")


def format_msg(bet):
    return (
        f"🔥 VIP TIP 🔥\n\n"
        f"⚽ {bet['teams']}\n"
        f"➡️ {bet['type'].upper()}\n"
        f"📈 Prob: {bet['prob']:.2%}\n"
        f"⭐ Confiança: {bet['confidence']:.2f}\n"
        f"💎 Score: {bet['score']:.3f}"
    )


def main():
    _, vip = run()
    bot = Bot(token=TOKEN)

    bot.send_message(chat_id=CHAT_ID, text="🔥 MELHORES OPORTUNIDADES (VIP)\n")

    for bet in vip:
        bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))


if __name__ == "__main__":
    main()
