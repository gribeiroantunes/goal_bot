import logging
import math

logger = logging.getLogger("market_analyzer")

MIN_PROB = 0.50
MIN_SCORE = 0.55
MAX_DIVERGENCE = 0.22


MARKET_WEIGHTS = {
    "Over 1.5": 1.0,
    "Over 2.5": 0.97,
    "Over 3.5": 0.90,
    "Under 2.5": 0.93,
    "BTTS": 0.96,
    "No BTTS": 0.92,
    "1": 0.90,
    "X": 0.80,
    "2": 0.90,
}


def calibrate_prob(p):
    try:
        logit = math.log(p / (1 - p))
        return max(0.05, min(1 / (1 + math.exp(-0.7 * logit)), 0.95))
    except:
        return p


def calculate_goal_trend(event):
    base = (
        event.get("home_avg_goals_scored", 1.3) +
        event.get("away_avg_goals_scored", 1.2)
    ) / 2

    return max(0.45, min(base / 2.5, 0.75))


def calculate_consistency(event):
    var = (
        event.get("home_goal_variance", 1.5) +
        event.get("away_goal_variance", 1.5)
    ) / 2

    return max(0.45, min(1 - (var / 5), 0.8))


def calculate_volatility(event):
    return (
        event.get("btts_freq", 0.5) +
        event.get("over_35_freq", 0.35)
    ) / 2


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
    edge = prob - 0.5

    if edge <= 0:
        return 0.5

    return max(1, min(edge * confidence * 10, 6))


def analyze_and_select(events_with_preds):

    selections = []

    for item in events_with_preds:
        event = item["event"]
        pred = item["prediction"]

        if event.get("status") != "notstarted":
            continue

        home = event.get("home_team", "Home")
        away = event.get("away_team", "Away")

        markets = [
            ("Over 1.5", pred.get("prob_over_15", 0) / 100),
            ("Over 2.5", pred.get("prob_over_25", 0) / 100),
            ("Over 3.5", pred.get("prob_over_35", 0) / 100),
            ("Under 2.5", pred.get("prob_under_25", 0) / 100),
            ("BTTS", pred.get("prob_btts_yes", 0) / 100),
            ("No BTTS", pred.get("prob_btts_no", 0) / 100),
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

            final_prob = build_final_prob(calibrate_prob(api_prob), trend)
            divergence = abs(api_prob - trend)

            if divergence > MAX_DIVERGENCE:
                continue

            confidence = build_confidence(api_conf, divergence, consistency)
            score = build_score(final_prob, confidence, consistency, volatility)

            score *= MARKET_WEIGHTS.get(market_name, 1)

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
                "event_date": event.get("event_date")
            })

    selections.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"Oportunidades: {len(selections)}")
    return selections
