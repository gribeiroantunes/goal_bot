import numpy as np
from scipy.stats import poisson

HOME_ADVANTAGE = 0.15
LEAGUE_AVG_GOALS = 2.5

FORM_WEIGHT = 0.7

def adjust_form(avg, recent):
    return (avg * (1 - FORM_WEIGHT)) + (recent * FORM_WEIGHT)
    
def calculate_lambda(home, away):
    attack_home = home["avg_goals_scored"] / LEAGUE_AVG_GOALS
    defense_home = home["avg_goals_conceded"] / LEAGUE_AVG_GOALS

    attack_away = away["avg_goals_scored"] / LEAGUE_AVG_GOALS
    defense_away = away["avg_goals_conceded"] / LEAGUE_AVG_GOALS

    lambda_home = attack_home * defense_away * LEAGUE_AVG_GOALS
    lambda_away = attack_away * defense_home * LEAGUE_AVG_GOALS

    lambda_home *= (1 + HOME_ADVANTAGE)

    return np.clip(lambda_home, 0.2, 4), np.clip(lambda_away, 0.2, 4)


def goal_matrix(lh, la, max_goals=6):
    matrix = np.zeros((max_goals, max_goals))

    for i in range(max_goals):
        for j in range(max_goals):
            matrix[i][j] = poisson.pmf(i, lh) * poisson.pmf(j, la)

    return matrix


def over_under(matrix, line=2.5):
    over = 0

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if i + j > line:
                over += matrix[i][j]

    return over, 1 - over


def analyze_match(home, away):
    lh, la = calculate_lambda(home, away)
    matrix = goal_matrix(lh, la)
    over, under = over_under(matrix)

    return {
        "prob_over": over,
        "prob_under": under
    }
