from config import WEIGHT_PROB, WEIGHT_EV


def rank_bets(bets):
    for bet in bets:
        # Score equilibrado + leve bias pra gerar picks
        bet["score"] = (
            (bet["prob"] * WEIGHT_PROB) +
            ((bet["ev"] + 0.03) * WEIGHT_EV)
        )

    return sorted(bets, key=lambda x: x["score"], reverse=True)


def split_free_vip(bets):
    ranked = rank_bets(bets)

    # 🔴 VIP = MELHORES
    vip = ranked[:3]

    # 🟢 FREE = BOAS (não as melhores)
    free = ranked[3:7]

    # fallback se poucos jogos
    if len(ranked) < 7:
        vip = ranked[:2]
        free = ranked[2:5]

    return free, vip
