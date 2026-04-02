def estimate_market_odds(prob):
    # simulação simples de mercado (ajustável)
    margin = 0.08
    odds = (1 / prob) * (1 - margin)
    return round(odds, 2)


def calculate_ev(prob, odds):
    return (prob * odds) - 1


def analyze_value(prob_over, prob_under):
    odds_over = estimate_market_odds(prob_over)
    odds_under = estimate_market_odds(prob_under)

    ev_over = calculate_ev(prob_over, odds_over)
    ev_under = calculate_ev(prob_under, odds_under)

    return {
        "over": {
            "prob": prob_over,
            "odds": odds_over,
            "ev": ev_over
        },
        "under": {
            "prob": prob_under,
            "odds": odds_under,
            "ev": ev_under
        }
    }
