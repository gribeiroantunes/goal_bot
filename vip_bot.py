import os
import asyncio
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003858302105

def is_high_quality(bet):
    return (
        bet["model_prob"] >= 0.65 and      # probabilidade alta
        bet["confidence"] >= 70 and        # confiança alta
        bet["expected_goals"] >= 2.2       # tendência ofensiva (importante!)
    )

def filter_vip(selections):
    vip = []

    for bet in selections:
        if (
            bet["model_prob"] >= 0.67 and
            bet["confidence"] >= 70 and
            bet["score"] >= 0.70
        ):
            bet["stake_pct"] = 6
            vip.append(bet)

    return vip[:5]


def format_msg(bets):
    msg = "💎 *ENTRADAS VIP - ALTA ASSERTIVIDADE*\n\n"

    for b in bets:
        msg += (
            f"⚽ {b['fixture_name']}\n"
            f"👉 {b['market']}\n"
            f"🔥 Prob: {b['model_prob']*100:.0f}%\n"
            f"💰 Stake: 5% a 7%\n\n"
        )

    msg += "⚠️ Gestão de banca obrigatória."

    return msg


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    merged = merge_events_predictions(events, preds)
    selections = analyze_and_select(merged)

    vip = filter_vip(selections)

    if not vip:
        await bot.send_message(CHANNEL_ID, "❌ Sem entradas premium hoje.")
        return

    await bot.send_message(CHANNEL_ID, format_msg(vip), parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())
