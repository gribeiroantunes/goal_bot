def estimate_odds(prob):
    # Simulação mais próxima do mercado real
    if prob >= 0.70:
        return 1.55
    elif prob >= 0.65:
        return 1.65
    elif prob >= 0.60:
        return 1.75
    elif prob >= 0.55:
        return 1.85
    else:
        return 2.00


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
