# value_calculator.py

from config import ODDS_MEDIA


def estimate_ev(prob, market):
    odd = ODDS_MEDIA.get(market, 1.75)
    return (prob * odd) - 1


def calculate_score(prob, ev, boost):
    return (
        prob * 0.5 +
        ev * 0.3 +
        boost * 0.2
    )
