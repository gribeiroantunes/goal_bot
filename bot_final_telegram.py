import logging
import asyncio
from datetime import datetime
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select
from telegram import Bot

# ---------------- CONFIG ----------------
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = "-1003725207734"
BANKROLL = 1000
TOP_N = 10
# ----------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")


# ---------------- HELPERS ----------------

def prob_label(p):
    if p >= 0.75:
        return "MUITO ALTA"
    elif p >= 0.65:
        return "ALTA"
    elif p >= 0.55:
        return "MODERADA"
    else:
        return "ARRISCADA"


def confidence_label(c):
    if c >= 75:
        return "ALTA"
    elif c >= 60:
        return "MÉDIA"
    else:
        return "BAIXA"


def stake_text(s):
    if s <= 1:
        return "Aposte bem leve (1%)"
    elif s <= 3:
        return "Aposte leve (2-3%)"
    elif s <= 5:
        return "Aposte médio (3-5%)"
    else:
        return "Aposte forte (5%+)"


def translate_market(market):
    if "Over" in market:
        return f"Mais de {market.split()[1]} gols"
    elif "Under" in market:
        return f"Menos de {market.split()[1]} gols"
    elif market == "BTTS":
        return "Ambas marcam"
    return market


# ---------------- FORMATADORES ----------------

def format_top_bet(bet):
    market_pt = translate_market(bet["market"])

    return (
        f"🏆 *APOSTA DO DIA* 🏆\n\n"
        f"⚽ *{bet['fixture_name']}*\n"
        f"👉 Mercado: *{market_pt}*\n\n"
        f"🔥 Chance: *{prob_label(bet['model_prob'])} ({bet['model_prob']*100:.0f}%)*\n"
        f"🧠 Segurança: *{confidence_label(bet['confidence'])}*\n"
        f"💰 {stake_text(bet['stake_pct'])}\n\n"
        f"📌 Forte tendência de gols.\n"
        f"━━━━━━━━━━━━━━━"
    )


def format_message(selections):
    today = datetime.now().strftime("%d/%m/%Y")
    msg = f"📊 *OPORTUNIDADES ({today})*\n\n"

    for bet in selections[:TOP_N]:
        market_pt = translate_market(bet["market"])

        msg += (
            f"⚽ *{bet['fixture_name']}*\n"
            f"👉 {market_pt}\n"
            f"✅ {prob_label(bet['model_prob'])}\n"
            f"💰 {stake_text(bet['stake_pct'])}\n\n"
        )

    msg += "⚠️ Gestão de banca é essencial."

    return msg


# ---------------- CORE ----------------

async def send(bot, msg):
    await bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")


def prepare():
    events = get_events_week()
    preds = get_predictions()
    merged = merge_events_predictions(events, preds)

    if not merged:
        return []

    return analyze_and_select(merged)


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    selections = prepare()

    if not selections:
        logger.info("Sem oportunidades hoje")
        return

    # 🏆 Aposta do dia (com filtro de qualidade)
    top = selections[0]

    if top["score"] >= 0.70 and top["confidence"] >= 65:
        await send(bot, format_top_bet(top))

    # 📊 Lista geral
    await send(bot, format_message(selections))


if __name__ == "__main__":
    asyncio.run(main())