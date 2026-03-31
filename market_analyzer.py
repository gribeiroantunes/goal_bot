import logging

logger = logging.getLogger("market_analyzer")

# ---------------- CONFIG ----------------
MIN_PROB = 0.55
MIN_SCORE = 0.60
MAX_DIVERGENCE = 0.15
# ----------------------------------------


def calibrate_prob(p):
    return 0.9 * p + 0.05


def calculate_goal_trend(event):
    return 0.6  # placeholder (pode evoluir depois)


def calculate_consistency(event):
    return 0.65  # placeholder


def calculate_volatility(event):
    return 0.4  # placeholder


def build_final_prob(api_prob, trend):
    return (0.7 * api_prob) + (0.3 * trend)


def build_confidence(api_conf, divergence, consistency):
    return (
        0.5 * api_conf +
        0.3 * (1 - divergence) +
        0.2 * consistency
    )


def build_score(prob, confidence, consistency, volatility):
    return (
        0.4 * prob +
        0.3 * confidence +
        0.2 * consistency +
        0.1 * (1 - volatility)
    )


def calculate_stake(prob, confidence):
    raw = (prob - 0.5) * 2
    return max(0.5, min(raw * confidence * 10, 10))


def analyze_and_select(events_with_preds):
    selections = []

    for item in events_with_preds:
        event = item["event"]
        pred = item["prediction"]

        home = event.get("home_team", "Home")
        away = event.get("away_team", "Away")

        markets = [
            ("Over 1.5", pred.get("prob_over_15", 0) / 100),
            ("Over 2.5", pred.get("prob_over_25", 0) / 100),
            ("Over 3.5", pred.get("prob_over_35", 0) / 100),
            ("BTTS", pred.get("prob_btts_yes", 0) / 100)
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

            selections.append({
                "fixture_name": f"{home} vs {away}",
                "market": market_name,
                "model_prob": round(final_prob, 3),
                "confidence": round(confidence * 100, 2),
                "score": round(score, 3),
                "stake_pct": round(stake, 2)
            })

    selections.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"Oportunidades finais: {len(selections)}")
    return selections