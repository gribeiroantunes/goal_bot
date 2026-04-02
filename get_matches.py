def get_matches():
    predictions = get_predictions()

    bets = []

    for p in predictions:
        try:
            event = p["event"]

            # 🔥 FILTRO MÍNIMO (CRÍTICO)
            if p["confidence"] < 0.55:
                continue

            # OVER 2.5
            if p.get("prob_over_25") and p["prob_over_25"] > 55:
                bets.append({
                    "type": "over_2.5",
                    "prob": p["prob_over_25"] / 100,
                    "confidence": p["confidence"],
                    "teams": f"{event['home_team']} vs {event['away_team']}"
                })

            # BTTS
            if p.get("prob_btts_yes") and p["prob_btts_yes"] > 55:
                bets.append({
                    "type": "btts",
                    "prob": p["prob_btts_yes"] / 100,
                    "confidence": p["confidence"],
                    "teams": f"{event['home_team']} vs {event['away_team']}"
                })

        except:
            continue

    print(f"Total bets geradas: {len(bets)}")
    return bets
