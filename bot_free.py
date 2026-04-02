# bot_free.py

import os
import asyncio
from telegram import Bot

from adaptive_model import adjust_probability
from value_calculator import estimate_ev, calculate_score
from history_manager import add_bet
from config import EV_MIN_FREE

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = -1003725207734


def get_games():
    # 👉 substitua pelo seu coletor real
    return [
        {
            "id": "1",
            "league": "EPL",
            "market": "over_2_5",
            "prob": 0.65,
            "home": "Team A",
            "away": "Team B"
        }
    ]


def select_bets(games):
    bets = []

    for game in games:
        base_prob = game["prob"]

        adj_prob = adjust_probability(base_prob, game["league"], game["market"])

        if adj_prob == 0:
            continue  # liga ruim

        ev = estimate_ev(adj_prob, game["market"])
        boost = adj_prob - base_prob
        score = calculate_score(adj_prob, ev, boost)

        if ev > EV_MIN_FREE and score > 0.60:
            game["prob"] = adj_prob
            game["ev"] = ev

            bets.append(game)
            add_bet(game)

    return bets


def format_msg(g):
    return (
        f"⚽ {g['home']} vs {g['away']}\n"
        f"📊 {g['market']}\n"
        f"📈 Prob: {g['prob']:.2%}\n"
        f"💰 EV: {g['ev']:.2f}"
    )


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    games = get_games()
    bets = select_bets(games)

    for b in bets:
        await bot.send_message(CHANNEL_ID, format_msg(b))


if __name__ == "__main__":
    asyncio.run(main())
