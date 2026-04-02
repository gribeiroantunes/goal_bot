def rank_bets(bets):
    for bet in bets:
        # Score mais inteligente
        bet["score"] = (
            bet["prob"] * 0.6 +
            bet["ev"] * 0.4
        )

    return sorted(bets, key=lambda x: x["score"], reverse=True)


def split_free_vip(bets):
    ranked = rank_bets(bets)

    # 🔴 VIP = MELHORES
    vip = ranked[:5]

    # 🟢 FREE = BOAS (mas não as top)
    free = ranked[5:10]

    # fallback caso poucos jogos
    if len(ranked) < 10:
        vip = ranked[:3]
        free = ranked[3:6]

    return free, vip
