def score_bet(bet):
    prob = float(bet.get("prob", 0))
    confidence = float(bet.get("confidence", 0))
    return round(prob * confidence, 6)


def market_label(market_type):
    labels = {
        "over_1.5": "Mais de 1.5 gols",
        "over_2.5": "Mais de 2.5 gols",
        "over_3.5": "Mais de 3.5 gols",
        "under_1.5": "Menos de 1.5 gols",
        "under_2.5": "Menos de 2.5 gols",
        "under_3.5": "Menos de 3.5 gols",
        "btts": "Ambas marcam",
        "no_btts": "Ambas não marcam",
        "home_win": "Time da casa vence",
        "draw": "Empate",
        "away_win": "Time visitante vence",
    }
    return labels.get(market_type, market_type.replace("_", " ").title())


def split_free_vip(bets):
    free_types = {
        "over_1.5",
        "over_2.5",
        "over_3.5",
        "under_1.5",
        "under_2.5",
        "under_3.5",
        "btts",
        "no_btts",
    }

    vip_types = free_types | {"home_win", "draw", "away_win"}

    enriched = []
    for bet in bets or []:
        b = dict(bet)
        b["score"] = score_bet(b)
        b["market"] = market_label(b.get("type", ""))
        enriched.append(b)

    enriched.sort(key=lambda x: x.get("score", 0), reverse=True)

    vip = [b for b in enriched if b.get("type") in vip_types][:3]
    free = [b for b in enriched if b.get("type") in free_types and b not in vip][:5]

    return free, vip
