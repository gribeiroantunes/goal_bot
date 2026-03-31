import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003725207734
VIP_LINK = "https://t.me/+ckOVtoDxOItmMzUx"
HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def get_last_7_days(data):
    cutoff = datetime.now() - timedelta(days=7)
    return [x for x in data if datetime.strptime(x["date"], "%Y-%m-%d") >= cutoff]


def calculate_stats(data):
    wins = sum(1 for x in data if x.get("result") == "win")
    losses = sum(1 for x in data if x.get("result") == "loss")
    total = wins + losses
    acc = (wins / total * 100) if total > 0 else 0
    return wins, losses, acc


def format_message(wins, losses, acc):
    return (
        f"📊 *RESULTADOS DOS ÚLTIMOS 7 DIAS*\n\n"
        f"✅ Wins: {wins}\n"
        f"❌ Losses: {losses}\n"
        f"📈 Assertividade: {acc:.1f}%\n\n"
        f"🔥 Método focado em consistência\n\n"
        f"💎 Quer entrar no próximo nível?\n"
        f"👉 Sinais com maior probabilidade\n"
        f"👉 Gestão de 5% a 7%\n\n"
        f"🚀 Entre no VIP:\n{VIP_LINK}"
    )


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    history = load_history()
    recent = get_last_7_days(history)

    wins, losses, acc = calculate_stats(recent)

    msg = format_message(wins, losses, acc)

    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.run(main())
