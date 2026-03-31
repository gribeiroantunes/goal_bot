import os
import asyncio
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003858302105


def filter_vip(selections):
    vip = []

    for bet in selections:
        if (
            bet["model_prob"] >= 0.64 and
            bet["confidence"] >= 65 and
            bet["score"] >= 0.65
        ):
            bet["stake_pct"] = 6
            vip.append(bet)

    # 🔥 NUNCA fica vazio
    if not vip:
        vip = selections[:3]

    return vip[:5]


def format_message(selections):
    msg = "💎 *ENTRADAS PREMIUM DO DIA*\n\n"

    msg += "🔥 *Alta probabilidade*\n"
    msg += "👉 Mercados: Gols + Resultado\n"
    msg += "👉 Entrada sugerida: *5% a 7% da banca*\n\n"

    for s in selections:
        msg += f"⚽ {s['fixture_name']}\n"
        msg += f"👉 {s['market']}\n"
        msg += f"📊 Chance: {int(s['model_prob']*100)}%\n"
        msg += f"💰 Stake: {s['stake_pct']}%\n\n"

    msg += "⚠️ Gestão de banca é essencial!"

    return msg


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions(events)
    data = merge_events_predictions(events, preds)

    selections = analyze_and_select(data)
    vip = filter_vip(selections)

    msg = format_message(vip)

    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.run(main())
