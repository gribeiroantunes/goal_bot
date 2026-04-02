def rank_bets(bets):
    for bet in bets:
        bet["score"] = (
            bet["prob"] * 0.6 +
            bet["confidence"] * 0.4
        )

    return sorted(bets, key=lambda x: x["score"], reverse=True)


def split_free_vip(bets):
    ranked = rank_bets(bets)

    vip = ranked[:5]
    free = ranked[5:10]

    if len(ranked) < 10:
        vip = ranked[:3]
        free = ranked[3:6]

    return free, vip
