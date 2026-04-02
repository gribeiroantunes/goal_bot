import numpy as np
from scipy.stats import poisson

LEAGUE_AVG_GOALS = {
    "default": 2.5
}

HOME_ADVANTAGE = 0.15

def get_league_avg(league):
    return LEAGUE_AVG_GOALS.get(league, LEAGUE_AVG_GOALS["default"])


def calculate_lambda(home, away, league="default"):
    league_avg = get_league_avg(league)

    attack_home = home["avg_goals_scored"] / league_avg
    defense_home = home["avg_goals_conceded"] / league_avg

    attack_away = away["avg_goals_scored"] / league_avg
    defense_away = away["avg_goals_conceded"] / league_avg

    lambda_home = attack_home * defense_away * league_avg
    lambda_away = attack_away * defense_home * league_avg

    # ajuste casa
    lambda_home *= (1 + HOME_ADVANTAGE)

    # limites realistas
    lambda_home = np.clip(lambda_home, 0.2, 4.0)
    lambda_away = np.clip(lambda_away, 0.2, 4.0)

    return lambda_home, lambda_away


def goal_probabilities(lambda_home, lambda_away, max_goals=6):
    matrix = np.zeros((max_goals, max_goals))

    for i in range(max_goals):
        for j in range(max_goals):
            matrix[i][j] = poisson.pmf(i, lambda_home) * poisson.pmf(j, lambda_away)

    return matrix


def over_under_probs(matrix, line=2.5):
    total_probs = 0
    over = 0

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            total = i + j
            prob = matrix[i][j]
            total_probs += prob

            if total > line:
                over += prob

    under = 1 - over

    return {
        "over": over,
        "under": under
    }


def analyze_match(home, away, league="default"):
    lambda_home, lambda_away = calculate_lambda(home, away, league)

    matrix = goal_probabilities(lambda_home, lambda_away)
    probs = over_under_probs(matrix)

    return {
        "lambda_home": lambda_home,
        "lambda_away": lambda_away,
        "prob_over": probs["over"],
        "prob_under": probs["under"]
    }
