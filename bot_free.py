import os
import asyncio
from telegram import Bot
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -100SEU_CANAL_FREE_AQUI  # 🔥 ALTERAR

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    events = get_events_week()
    preds = get_predictions()
    merged = merge_events_predictions(events, preds)
    selections = analyze_and_select(merged)

    if not selections:
        await bot.send_message(CHANNEL_ID, "❌ Nenhuma oportunidade hoje.")
        return

    msg = "📊 *OPORTUNIDADES DO DIA*\n\n"

    for s in selections[:8]:
        msg += (
            f"⚽ {s['fixture_name']}\n"
            f"👉 {s['market']}\n"
            f"🔥 Prob: {s['model_prob']*100:.0f}%\n\n"
        )

    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(main())