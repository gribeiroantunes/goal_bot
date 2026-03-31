import os
import asyncio
from datetime import datetime, timezone, timedelta
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003858302105


from datetime import datetime, timezone, timedelta


def formatar_data_api(event_date_str):
    try:
        if not event_date_str:
            return "Horário indefinido"

        # 🔥 corrige formato +0400 → +04:00
        if event_date_str[-3] != ":":
            event_date_str = event_date_str[:-2] + ":" + event_date_str[-2:]

        dt = datetime.fromisoformat(event_date_str)

        brasil = dt.astimezone(timezone(timedelta(hours=-3)))

        return brasil.strftime("%d/%m às %H:%M")

    except Exception as e:
        print("Erro ao converter:", event_date_str, e)
        return "Horário indefinido"


def traduzir_mercado(m):
    mapa = {
        "Over 1.5": "Gols: Mais que 1.5",
        "Over 2.5": "Gols: Mais que 2.5",
        "Over 3.5": "Gols: Mais que 3.5",
        "BTTS": "Ambos marcam",
        "1": "Time da casa para vencer",
        "X": "Empate",
        "2": "Time visitante para vencer"
    }
    return mapa.get(m, m)


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

    # 🔥 nunca fica vazio
    if not vip:
        vip = selections[:3]

    return vip[:5]


def format_message(selections):
    msg = "💎 *ENTRADAS PREMIUM DO DIA*\n\n"

    msg += "🔥 Alta probabilidade\n"
    msg += "👉 Gols + Resultado\n"
    msg += "👉 Entrada: 5% a 7% da banca\n\n"

    for s in selections:
        msg += f"⚽ {s['fixture_name']}\n"
        msg += f"🕒 {formatar_data_api(s.get('event_date'))}\n"
        msg += f"👉 {traduzir_mercado(s['market'])}\n"
        msg += f"📊 Chance: {int(s['model_prob']*100)}%\n"
        msg += f"💰 Stake: {s['stake_pct']}%\n\n"

    msg += "⚠️ Gestão de banca é essencial!"

    return msg


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    data = merge_events_predictions(events, preds)

    selections = analyze_and_select(data)
    vip = filter_vip(selections)

    msg = format_message(vip)

    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.run(main())
