# adaptive_model.py

from history_manager import load_history
from config import MIN_GAMES_FOR_LEARNING


def get_performance(key, value):
    data = load_history()

    filtered = [
        x for x in data
        if x.get(key) == value and x.get("result") != "pending"
    ]

    if len(filtered) < MIN_GAMES_FOR_LEARNING:
        return 0.5

    wins = sum(1 for x in filtered if x["result"] == "win")
    return wins / len(filtered)


def adjust_probability(base_prob, league, market):
    league_perf = get_performance("league", league)
    market_perf = get_performance("market", market)

    adjusted = (
        base_prob * 0.6 +
        league_perf * 0.2 +
        market_perf * 0.2
    )

    return max(0, min(1, adjusted))
