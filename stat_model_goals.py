# stat_model_goals.py
import math
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List
from scipy.stats import poisson

logger = logging.getLogger("stat_model_goals")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s — %(message)s")

# ---------- Estruturas ----------
@dataclass
class TeamProfile:
    team_id: int
    team_name: str
    avg_goals_for: float
    avg_goals_against: float
    last_5_goals: Optional[List[float]] = None
    recent_form_factor: float = 1.0

@dataclass
class MatchPrediction:
    fixture_id: int
    home_team: str
    away_team: str
    lambda_home: float
    lambda_away: float
    prob_over: dict = field(default_factory=dict)
    prob_under: dict = field(default_factory=dict)
    confidence_score: float = 0.0

# ---------- Constantes ----------
LEAGUE_AVG_GOALS = 2.5
HOME_ADVANTAGE_GOALS = 1.08

# ---------- Lambda Goals ----------
def estimate_lambda_goals(home: TeamProfile, away: TeamProfile):
    base_home = (home.avg_goals_for + np.mean(home.last_5_goals or [home.avg_goals_for])) / 2
    base_away = (away.avg_goals_for + np.mean(away.last_5_goals or [away.avg_goals_for])) / 2

    raw_home = base_home * away.avg_goals_against / LEAGUE_AVG_GOALS
    raw_away = base_away * home.avg_goals_against / LEAGUE_AVG_GOALS

    lambda_home = raw_home * HOME_ADVANTAGE_GOALS * home.recent_form_factor
    lambda_away = raw_away * (1 / HOME_ADVANTAGE_GOALS) * away.recent_form_factor

    lambda_home = np.clip(np.random.normal(lambda_home, 0.25), 0.3, 4.5)
    lambda_away = np.clip(np.random.normal(lambda_away, 0.25), 0.3, 4.5)

    return round(lambda_home, 2), round(lambda_away, 2)

# ---------- Probabilidades ----------
def prob_over_goals(line: float, lam_home: float, lam_away: float) -> float:
    lam_total = lam_home + lam_away
    return 1 - poisson.cdf(math.floor(line), lam_total)

def prob_under_goals(line: float, lam_home: float, lam_away: float) -> float:
    lam_total = lam_home + lam_away
    return poisson.cdf(math.floor(line), lam_total)

# ---------- Confiança ----------
def calculate_confidence(home: TeamProfile, away: TeamProfile):
    var_home = np.std(home.last_5_goals) if home.last_5_goals else 1.0
    var_away = np.std(away.last_5_goals) if away.last_5_goals else 1.0
    total_var = var_home + var_away
    conf_score = max(0, min(100, 100 - total_var*15))
    return conf_score

# ---------- Previsão ----------
def predict_match(fixture_id, home_team, away_team, home_profile, away_profile, lines=None):
    if lines is None:
        lines = [1.5, 2.5, 3.5]

    lambda_home, lambda_away = estimate_lambda_goals(home_profile, away_profile)

    prob_over_map = {line: prob_over_goals(line, lambda_home, lambda_away) for line in lines}
    prob_under_map = {line: prob_under_goals(line, lambda_home, lambda_away) for line in lines}

    confidence_score = calculate_confidence(home_profile, away_profile)

    return MatchPrediction(
        fixture_id=fixture_id,
        home_team=home_team,
        away_team=away_team,
        lambda_home=lambda_home,
        lambda_away=lambda_away,
        prob_over=prob_over_map,
        prob_under=prob_under_map,
        confidence_score=confidence_score
    )