import logging

logger = logging.getLogger("market_analyzer")

MIN_PROB = 0.55
MIN_SCORE = 0.60
MAX_DIVERGENCE = 0.18


def calibrate_prob(p):
    return 0.92 * p + 0.04


# 🔥 AGORA BASEADO EM DADOS
def calculate_goal_trend(event):
    home_goals = event.get("home_goals_avg", 1.4)
    away_goals = event.get("away_goals_avg", 1.2)

    total = home_goals + away_goals

    # normaliza entre 0 e 1
    return min(total / 4, 1)


def calculate_consistency(event):
    home_form = event.get("home_form", 0.5)
    away_form = event.get("away_form", 0.5)

    return (home_form + away_form) / 2


def calculate_volatility(event):
    return event.get("volatility", 0.4)


def build_final_prob(api_prob, trend):
    return (0.75 * api_prob) + (0.25 * trend)


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
    return max(1, min(raw * confidence * 10, 10))


def analyze_and_select(events_with_preds):
    selections = []

    for item in events_with_preds:
        event = item["event"]
        pred = item["prediction"]

        home = event.get("home_team", "Home")
        away = event.get("away_team", "Away")

        # 🔥 AGORA COM RESULTADO TAMBÉM
        markets = [
            ("Over 1.5", pred.get("prob_over_15", 0) / 100),
            ("Over 2.5", pred.get("prob_over_25", 0) / 100),
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

            selections.append({
                "fixture_name": f"{home} vs {away}",
                "market": market_name,
                "model_prob": round(final_prob, 3),
                "confidence": round(confidence * 100, 2),
                "score": round(score, 3),
                "stake_pct": round(stake, 2),
                "expected_goals": trend * 3.5  # 🔥 usado no VIP
            })

    selections.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"Oportunidades finais: {len(selections)}")
    return selections
