import os
import asyncio
from datetime import datetime, timezone, timedelta
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003725207734


# 🔥 converter horário da API → Brasil
def formatar_data_api(event_date_str):
    try:
        dt = datetime.strptime(event_date_str, "%Y-%m-%dT%H:%M:%S%z")
        brasil = dt.astimezone(timezone(timedelta(hours=-3)))
        return brasil.strftime("%d/%m às %H:%M")
    except:
        return "Horário indefinido"


# 🔥 traduz mercados para linguagem simples
def traduzir_mercado(m):
    mapa = {
        "Over 1.5": "Gols: Mais que 1.5",
        "Over 2.5": "Gols: Mais que 2.5",
        "Over 3.5": "Gols: Mais que 3.5",
        "BTTS": "Ambos marcam"
    }
    return mapa.get(m, m)


def format_message(selections):
    msg = "📊 *OPORTUNIDADES DE GOLS DO DIA*\n\n"

    msg += "💡 Dicas simples:\n"
    msg += "👉 Foque apenas em gols\n"
    msg += "👉 Use de 2% a 3% da banca\n\n"

    count = 0

    for s in selections:

        # 🔥 só mercados de gols
        if s["market"] not in ["Over 1.5", "Over 2.5", "Over 3.5", "BTTS"]:
            continue

        msg += f"⚽ {s['fixture_name']}\n"
        msg += f"🕒 {formatar_data_api(s.get('event_date'))}\n"
        msg += f"👉 {traduzir_mercado(s['market'])}\n"
        msg += f"📊 Chance: {int(s['model_prob']*100)}%\n\n"

        count += 1
        if count >= 7:
            break

    msg += "💎 Quer sinais mais fortes?\n"
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
