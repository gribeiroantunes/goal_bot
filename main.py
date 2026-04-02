from data_collector import get_matches
from ranking import split_free_vip


def run():
    bets = get_matches() or []

    if len(bets) < 5:
        print("⚠️ Poucas bets da API, usando fallback híbrido")
        fallback = [
            {"type": "over_2.5", "prob": 0.62, "confidence": 0.70, "teams": "Game A"},
            {"type": "btts", "prob": 0.60, "confidence": 0.68, "teams": "Game B"},
            {"type": "under_2.5", "prob": 0.58, "confidence": 0.66, "teams": "Game C"},
            {"type": "no_btts", "prob": 0.57, "confidence": 0.65, "teams": "Game D"},
            {"type": "home_win", "prob": 0.59, "confidence": 0.67, "teams": "Game E"},
        ]
        bets.extend(fallback)

    free, vip = split_free_vip(bets)

    print(f"FREE: {len(free)} | VIP: {len(vip)}")
    return free, vip
