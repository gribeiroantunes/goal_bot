# bot_vip.py
import os
import asyncio
from datetime import datetime, timezone, timedelta
from telegram import Bot

from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003858302105


# ---------------- FORMATADORES ----------------

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


# ---------------- VIP (TOP PICKS) ----------------

def filter_vip(selections):
    ordered = sorted(selections, key=lambda x: x["score"], reverse=True)

    vip = []

    for bet in ordered:

        if bet["model_prob"] >= 0.60 and bet["confidence"] >= 60:

            if bet["model_prob"] >= 0.75:
                bet["stake_pct"] = 7
            elif bet["model_prob"] >= 0.70:
                bet["stake_pct"] = 6
            else:
                bet["stake_pct"] = 5

            vip.append(bet)

        if len(vip) >= 5:
            break

    if not vip:
        vip = ordered[:3]
        for v in vip:
            v["stake_pct"] = 5

    return vip


# ---------------- MENSAGEM ----------------

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


# ---------------- MAIN ----------------

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    data = merge_events_predictions(events, preds)

    selections = analyze_and_select(data)

    print(f"Selections: {len(selections)}")

    vip = filter_vip(selections)

    print(f"VIP: {len(vip)}")

    if not vip:
        await bot.send_message(
            CHANNEL_ID,
            "⚠️ Nenhuma entrada premium hoje.\nGestão acima de tudo."
        )
        return

    await bot.send_message(
        CHANNEL_ID,
        format_message(vip),
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    asyncio.run(main())
