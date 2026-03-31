import os
import asyncio
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003725207734


def format_message(selections):
    msg = "📊 *OPORTUNIDADES DO DIA (GOLS)*\n\n"

    msg += "💡 *Dicas simples para hoje*\n"
    msg += "👉 Foco apenas em gols\n"
    msg += "👉 Entrada sugerida: *2% a 3% da banca*\n\n"

    for s in selections[:7]:

        # 🔥 só gols
        if s["market"] not in ["Over 1.5", "Over 2.5", "BTTS"]:
            continue

        msg += f"⚽ {s['fixture_name']}\n"
        msg += f"👉 {s['market']}\n"
        msg += f"📊 Chance: {int(s['model_prob']*100)}%\n\n"

    msg += "💎 Quer entradas mais fortes?\n"
    msg += "👉 Entre no VIP:\n"
    msg += "https://t.me/+ckOVtoDxOItmMzUx"

    return msg


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    data = merge_events_predictions(events, preds)

    selections = analyze_and_select(data)

    msg = format_message(selections)

    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.run(main())
