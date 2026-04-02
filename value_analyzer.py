def estimate_odds(prob):
    margin = 0.08
    return round((1 / prob) * (1 - margin), 2)


def calculate_ev(prob, odds):
    return (prob * odds) - 1


def analyze_value(prob_over, prob_under):
    odds_over = estimate_odds(prob_over)
    odds_under = estimate_odds(prob_under)

    return {
        "over": {
            "prob": prob_over,
            "odds": odds_over,
            "ev": calculate_ev(prob_over, odds_over)
        },
        "under": {
            "prob": prob_under,
            "odds": odds_under,
            "ev": calculate_ev(prob_under, odds_under)
        }
    }
