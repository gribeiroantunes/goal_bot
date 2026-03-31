# data_collector.py
import os
import requests
import logging
from datetime import date, timedelta

logger = logging.getLogger("data_collector")

API_KEY = os.environ.get("BZ_API_KEY", "")
BASE_URL = "https://sports.bzzoiro.com/api"
HEADERS = {"Authorization": f"Token {API_KEY}"} if API_KEY else {}

def get_events_week(days_ahead: int = 7):
    if not API_KEY:
        logger.error("API key não configurada.")
        return []

    start = date.today()
    end = start + timedelta(days=days_ahead)
    params = {"date_from": start.isoformat(), "date_to": end.isoformat()}

    try:
        r = requests.get(f"{BASE_URL}/events/", headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        events = data.get("results", [])
        logger.info(f"Eventos válidos coletados da API: {len(events)}")
        return events
    except requests.RequestException as e:
        logger.error(f"Erro ao coletar eventos: {e}")
        return []

def get_predictions():
    if not API_KEY:
        logger.error("API key não configurada.")
        return []

    try:
        r = requests.get(f"{BASE_URL}/predictions/", headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        preds = data.get("results", [])
        logger.info(f"Previsões coletadas: {len(preds)} jogos")
        return preds
    except requests.RequestException as e:
        logger.error(f"Erro ao coletar previsões: {e}")
        return []

def merge_events_predictions(events, predictions):
    merged = []
    pred_map = {p.get("event", {}).get("id"): p for p in predictions if p.get("event", {}).get("id")}
    for e in events:
        eid = e.get("id")
        pred = pred_map.get(eid)
        if pred:
            merged.append({"event": e, "prediction": pred})
    logger.info(f"Eventos processados com forecasts: {len(merged)}")
    return merged