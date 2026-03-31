def filter_vip(selections, free):
    vip = []

    free_keys = {(f["fixture_name"], f["market"]) for f in free}

    # base do FREE
    max_free_score = max([s["score"] for s in free], default=0)

    for bet in selections:

        if (bet["fixture_name"], bet["market"]) in free_keys:
            continue

        if bet["score"] >= max_free_score + 0.02:

            if bet["model_prob"] >= 0.75:
                bet["stake_pct"] = 7
            elif bet["model_prob"] >= 0.70:
                bet["stake_pct"] = 6
            else:
                bet["stake_pct"] = 5

            vip.append(bet)

    if not vip:
        vip = [
            s for s in selections
            if (s["fixture_name"], s["market"]) not in free_keys
        ][:3]

        for v in vip:
            v["stake_pct"] = 5

    return vip[:5]
