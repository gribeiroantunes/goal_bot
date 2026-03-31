import os
import asyncio
from datetime import datetime, timezone, timedelta
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select
from bot_free import filter_free

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003858302105


def formatar_data_api(event_date_str):
    try:
        if event_date_str[-3] != ":":
            event_date_str = event_date_str[:-2] + ":" + event_date_str[-2:]

        dt = datetime.fromisoformat(event_date_str)
        brasil = dt.astimezone(timezone(timedelta(hours=-3)))

        return brasil.strftime("%d/%m às %H:%M")
    except:
        return "Horário indefinido"


def traduzir_mercado(m):
    mapa = {
        "Over 1.5": "Gols: Mais que 1.5",
        "Over 2.5": "Gols: Mais que 2.5",
        "Over 3.5": "Gols: Mais que 3.5",
        "Under 2.5": "Gols: Menos que 2.5",
        "BTTS": "Ambos marcam",
        "No BTTS": "Ambos NÃO marcam",
        "1": "Time da casa vence",
        "X": "Empate",
        "2": "Time visitante vence"
    }
    return mapa.get(m, m)


def filter_vip(selections, free):
    free_keys = {(s["fixture_name"], s["market"]) for s in free}
    vip = []

    for s in selections:
        key = (s["fixture_name"], s["market"])

        if key in free_keys:
            continue

        if s["model_prob"] >= 0.67 and s["confidence"] >= 70 and s["score"] >= 0.70:
            s["stake_pct"] = 6
            vip.append(s)

    if not vip:
        for s in selections:
            key = (s["fixture_name"], s["market"])
            if key not in free_keys:
                vip.append(s)

    return vip[:5]


def format_message(selections):
    msg = "💎 *ENTRADAS PREMIUM*\n\n"
    msg += "👉 Use 5% a 7% da banca\n\n"

    for s in selections:
        msg += f"⚽ {s['fixture_name']}\n"
        msg += f"🕒 {formatar_data_api(s.get('event_date'))}\n"
        msg += f"👉 {traduzir_mercado(s['market'])}\n"
        msg += f"📊 Chance: {int(s['model_prob']*100)}%\n"
        msg += f"💰 Stake: {s['stake_pct']}%\n\n"

    return msg


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    data = merge_events_predictions(events, preds)

    selections = analyze_and_select(data)

    free = filter_free(selections)
    vip = filter_vip(selections, free)

    await bot.send_message(CHANNEL_ID, format_message(vip), parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.run(main())
