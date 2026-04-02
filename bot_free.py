# bot_free.py

import os
import asyncio
from telegram import Bot

from value_calculator import estimate_ev, calculate_score
from adaptive_model import adjust_probability
from history_manager import add_bet, create_bet_entry
from config import EV_MIN_FREE

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -100XXXXXXXXX  # ajuste


def get_games():
    # ⚠️ SUBSTITUIR pelo seu coletor real
    return [
        {"id": "1", "league": "EPL", "market": "over_2_5", "prob": 0.65, "home": "A", "away": "B"}
    ]


def select_bets(games):
    selected = []

    for game in games:
        base_prob = game["prob"]

        adj_prob = adjust_probability(base_prob, game["league"], game["market"])
        ev = estimate_ev(adj_prob, game["market"])
        boost = adj_prob - base_prob
        score = calculate_score(adj_prob, ev, boost)

        if ev > EV_MIN_FREE and score > 0.60:
            game["prob"] = adj_prob
            game["ev"] = ev

            selected.append(game)
            add_bet(create_bet_entry(game))

    return selected


def format_msg(game):
    return (
        f"⚽ {game['home']} vs {game['away']}\n"
        f"📊 Mercado: {game['market']}\n"
        f"📈 Prob: {game['prob']:.2%}\n"
        f"💰 EV: {game['ev']:.2f}"
    )


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    games = get_games()
    bets = select_bets(games)

    for bet in bets:
        await bot.send_message(CHANNEL_ID, format_msg(bet))


if __name__ == "__main__":
    asyncio.run(main())
