def filter_vip(selections, free):
    vip = []

    free_keys = {(f["fixture_name"], f["market"]) for f in free}

    max_free_score = max([s["score"] for s in free], default=0)
    max_free_prob = max([s["model_prob"] for s in free], default=0)

    for bet in selections:

        # 🚫 nunca repetir FREE
        if (bet["fixture_name"], bet["market"]) in free_keys:
            continue

        # 🔥 regra VIP (melhor OU equivalente)
        if (
            bet["score"] >= max_free_score - 0.01 and
            bet["model_prob"] >= max_free_prob - 0.02
        ):

            if bet["model_prob"] >= 0.75:
                bet["stake_pct"] = 7
            elif bet["model_prob"] >= 0.70:
                bet["stake_pct"] = 6
            else:
                bet["stake_pct"] = 5

            vip.append(bet)

    # 🔥 fallback FORTE (garante envio sempre)
    if not vip:
        vip = [
            s for s in selections
            if (s["fixture_name"], s["market"]) not in free_keys
        ]

        vip = sorted(vip, key=lambda x: x["score"], reverse=True)[:3]

        for v in vip:
            v["stake_pct"] = 5

    return vip[:5]
