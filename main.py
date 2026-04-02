from data_collector import get_matches
from ranking import split_free_vip


def run():
    bets = get_matches()

    if not bets:
        print("⚠️ Sem dados da API")

        # fallback mínimo
        bets = [
            {"type": "over_2.5", "prob": 0.60, "confidence": 0.7, "teams": "Fallback Game"}
        ]

    free, vip = split_free_vip(bets)

    return free, vip
