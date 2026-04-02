# adaptive_model.py

from history_manager import load_history
from config import MIN_GAMES_FOR_LEARNING, MIN_LEAGUE_PERFORMANCE


def filter_data(key, value):
    data = load_history()
    return [x for x in data if x.get(key) == value and x["result"] != "pending"]


def win_rate(data):
    if len(data) == 0:
        return 0.5
    wins = sum(1 for x in data if x["result"] == "win")
    return wins / len(data)


def get_league_performance(league):
    data = filter_data("league", league)

    if len(data) < MIN_GAMES_FOR_LEARNING:
        return 0.5

    return win_rate(data)


def get_market_performance(market):
    data = filter_data("market", market)

    if len(data) < MIN_GAMES_FOR_LEARNING:
        return 0.5

    return win_rate(data)


def adjust_probability(base_prob, league, market):
    league_perf = get_league_performance(league)
    market_perf = get_market_performance(market)

    # corta liga ruim automaticamente
    if league_perf < MIN_LEAGUE_PERFORMANCE:
        return 0  # bloqueia aposta

    adjusted = (
        base_prob * 0.6 +
        league_perf * 0.2 +
        market_perf * 0.2
    )

    return max(0, min(1, adjusted))
