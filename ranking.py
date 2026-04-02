def score_bet(bet):
    prob = float(bet.get("prob", 0))
    confidence = float(bet.get("confidence", 0))
    return round((prob * confidence), 4)


def split_free_vip(bets):
    free_allowed = {
        "over_1.5",
        "over_2.5",
        "over_3.5",
        "under_1.5",
        "under_2.5",
        "under_3.5",
        "btts",
        "no_btts",
    }

    vip_allowed = free_allowed | {
        "home_win",
        "draw",
        "away_win",
    }

    enriched = []
    for bet in bets or []:
        bet = dict(bet)
        bet["score"] = score_bet(bet)
        enriched.append(bet)

    enriched.sort(key=lambda x: x.get("score", 0), reverse=True)

    free = [b for b in enriched if b.get("type") in free_allowed]
    vip = [b for b in enriched if b.get("type") in vip_allowed and b.get("type") not in free_allowed]

    vip.extend([b for b in enriched if b.get("type") in {"home_win", "draw", "away_win"}])

    vip.sort(key=lambda x: x.get("score", 0), reverse=True)

    return free, vip
