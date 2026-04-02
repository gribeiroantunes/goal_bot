import os
from datetime import datetime, timedelta
from telegram import Bot

from history_manager import load_history

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHAT_ID_FREE")
VIP_LINK = os.getenv("VIP_LINK", "https://t.me/seu_link_vip_aqui")


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        return None


def last_7_days(data):
    cutoff = datetime.now() - timedelta(days=7)
    recent = []
    for x in data:
        d = parse_date(x.get("date", ""))
        if d is None:
            continue
        if d >= cutoff and x.get("result") != "pending":
            recent.append(x)
    return recent


def stats(data):
    wins = sum(1 for x in data if x.get("result") == "win")
    losses = sum(1 for x in data if x.get("result") == "loss")
    total = wins + losses
    acc = (wins / total * 100) if total > 0 else 0
    roi = sum(float(x.get("ev", 0)) for x in data)
    return wins, losses, acc, roi


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN não encontrado no ambiente")
    if not CHANNEL_ID:
        raise ValueError("TELEGRAM_CHAT_ID_FREE não encontrado no ambiente")

    bot = Bot(token=TELEGRAM_TOKEN)

    data = load_history()
    recent = last_7_days(data)

    w, l, acc, roi = stats(recent)

    msg = (
        f"📊 REPORT DOS ÚLTIMOS 7 DIAS\n\n"
        f"✅ Wins: {w}\n"
        f"❌ Losses: {l}\n"
        f"📈 Assertividade: {acc:.1f}%\n"
        f"💰 ROI acumulado: {roi:.2f}\n\n"
        f"🔒 Quer acesso ao VIP?\n"
        f"{VIP_LINK}"
    )

    bot.send_message(chat_id=CHANNEL_ID, text=msg)


if __name__ == "__main__":
    main()
