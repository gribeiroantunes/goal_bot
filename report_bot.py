# report_bot.py

import os
import asyncio
from datetime import datetime, timedelta
from telegram import Bot

from history_manager import load_history

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -100XXXXXXXXX


def last_7_days(data):
    cutoff = datetime.now() - timedelta(days=7)
    return [
        x for x in data
        if datetime.strptime(x["date"], "%Y-%m-%d") >= cutoff
        and x["result"] != "pending"
    ]


def stats(data):
    wins = sum(1 for x in data if x["result"] == "win")
    losses = sum(1 for x in data if x["result"] == "loss")
    total = wins + losses

    acc = (wins / total * 100) if total > 0 else 0
    roi = sum(x["ev"] for x in data)

    return wins, losses, acc, roi


def best_league(data):
    leagues = {}

    for x in data:
        lg = x["league"]
        leagues.setdefault(lg, {"w": 0, "t": 0})

        if x["result"] == "win":
            leagues[lg]["w"] += 1

        leagues[lg]["t"] += 1

    best = "N/A"
    best_rate = 0

    for lg, val in leagues.items():
        rate = val["w"] / val["t"]
        if rate > best_rate:
            best_rate = rate
            best = lg

    return best


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    data = load_history()
    recent = last_7_days(data)

    w, l, acc, roi = stats(recent)
    best = best_league(recent)

    msg = (
        f"📊 RESULTADOS 7 DIAS\n\n"
        f"✅ {w}W | ❌ {l}L\n"
        f"📈 {acc:.1f}%\n"
        f"💰 ROI: {roi:.2f}\n\n"
        f"🔥 Liga destaque: {best}"
    )

    await bot.send_message(CHANNEL_ID, msg)


if __name__ == "__main__":
    asyncio.run(main())
