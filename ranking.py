def rank_bets(bets):
    for bet in bets:
        bet["score"] = bet["prob"] * bet["ev"]

    return sorted(bets, key=lambda x: x["score"], reverse=True)


def split_free_vip(bets):
    ranked = rank_bets(bets)

    free = ranked[:2]
    vip = ranked[:5]

    return free, vip
