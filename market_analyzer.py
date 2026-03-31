for item in events_with_preds:
    event = item["event"]
    pred = item["prediction"]

    # 🚫 IGNORA jogos já iniciados
    if event.get("status") != "notstarted":
        continue

    home = event.get("home_team", "Home")
    away = event.get("away_team", "Away")

    markets = [
        ("Over 1.5", pred.get("prob_over_15", 0) / 100),
        ("Over 2.5", pred.get("prob_over_25", 0) / 100),
        ("Over 3.5", pred.get("prob_over_35", 0) / 100),
        ("BTTS", pred.get("prob_btts_yes", 0) / 100),
        ("1", pred.get("prob_home_win", 0) / 100),
        ("X", pred.get("prob_draw", 0) / 100),
        ("2", pred.get("prob_away_win", 0) / 100),
    ]

    api_conf = pred.get("confidence", 50) / 100

    trend = calculate_goal_trend(event)
    consistency = calculate_consistency(event)
    volatility = calculate_volatility(event)

    for market_name, api_prob in markets:

        if api_prob < MIN_PROB:
            continue

        calibrated = calibrate_prob(api_prob)
        final_prob = build_final_prob(calibrated, trend)

        divergence = abs(api_prob - trend)

        if divergence > MAX_DIVERGENCE:
            continue

        confidence = build_confidence(api_conf, divergence, consistency)
        score = build_score(final_prob, confidence, consistency, volatility)

        if score < MIN_SCORE:
            continue

        stake = calculate_stake(final_prob, confidence)

        # 🔥 AQUI ESTAVA O ERRO
        selections.append({
            "fixture_name": f"{home} vs {away}",
            "market": market_name,
            "model_prob": round(final_prob, 3),
            "confidence": round(confidence * 100, 2),
            "score": round(score, 3),
            "stake_pct": round(stake, 2),
            "expected_goals": trend * 3.5,
            "event_date": event.get("event_date")
        })
