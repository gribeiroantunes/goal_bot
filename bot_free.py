import os
from main import run
from data_collector import get_matches
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
from config import TELEGRAM_CHAT_ID_FREE as CHAT_ID


def format_msg(bet):
    return (
        f"📊 FREE TIP\n\n"
        f"➡️ {bet['type'].upper()}\n"
        f"📈 Prob: {bet['prob']:.2%}\n"
        f"💰 Odds: {bet['odds']}\n"
        f"📊 EV: {bet['ev']:.2f}"
    )


def main():
    matches = get_matches()
    free, _ = run(matches)

    bot = Bot(token=TOKEN)

    if not free:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Sem oportunidades hoje.")
        return

    for bet in free:
        bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))


if __name__ == "__main__":
    main()
