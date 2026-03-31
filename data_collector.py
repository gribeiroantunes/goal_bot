# data_collector.py
import os
import requests
import logging
from datetime import date, timedelta

logger = logging.getLogger("data_collector")

API_KEY = os.environ.get("BZ_API_KEY", "")
BASE_URL = "https://sports.bzzoiro.com/api"
HEADERS = {"Authorization": f"Token {API_KEY}"} if API_KEY else {}

TIMEOUT = 10


def safe_get(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.error(f"Erro na requisição {url}: {e}")
        return {}


def get_events_week(days_ahead: int = 7):
    if not API_KEY:
        logger.error("API key não configurada.")
        return []

    start = date.today()
    end = start + timedelta(days=days_ahead)

    params = {
        "date_from": start.isoformat(),
        "date_to": end.isoformat()
    }

    data = safe_get(f"{BASE_URL}/events/", params)

    events = data.get("results", [])

    logger.info(f"Eventos válidos coletados da API: {len(events)}")
    return events


def get_predictions():
    if not API_KEY:
        logger.error("API key não configurada.")
        return []

    data = safe_get(f"{BASE_URL}/predictions/")
    preds = data.get("results", [])

    logger.info(f"Previsões coletadas: {len(preds)} jogos")
    return preds


def enrich_event(event):
    """
    Prepara o evento para análise avançada.
    NÃO quebra compatibilidade com sua estrutura.
    """

    stats = event.get("stats", {}) or {}

    event["home_avg_goals_scored"] = stats.get("home_avg_goals_scored", 1.2)
    event["away_avg_goals_scored"] = stats.get("away_avg_goals_scored", 1.1)

    event["home_avg_goals_conceded"] = stats.get("home_avg_goals_conceded", 1.1)
    event["away_avg_goals_conceded"] = stats.get("away_avg_goals_conceded", 1.2)

    event["home_goal_variance"] = stats.get("home_goal_variance", 1.2)
    event["away_goal_variance"] = stats.get("away_goal_variance", 1.2)

    event["btts_freq"] = stats.get("btts_freq", 0.5)
    event["over_35_freq"] = stats.get("over_35_freq", 0.3)

    return event


def merge_events_predictions(events, predictions):
    merged = []

    pred_map = {
        p.get("event", {}).get("id"): p
        for p in predictions
        if p.get("event", {}).get("id")
    }

    for e in events:
        eid = e.get("id")
        pred = pred_map.get(eid)

        if pred:
            enriched_event = enrich_event(e)

            merged.append({
                "event": enriched_event,
                "prediction": pred
            })

    logger.info(f"Eventos processados com forecasts: {len(merged)}")
    return merged
