import os
import requests

API_KEY = os.getenv("BZ_API_KEY")
BASE_URL = "https://sports.bzzoiro.com/api"


def get_predictions():
    if not API_KEY:
        raise ValueError("BZ_API_KEY não encontrada no ambiente")

    headers = {"Authorization": f"Token {API_KEY}"}
    all_preds = []
    url = f"{BASE_URL}/predictions/?tz=America/Sao_Paulo"

    try:
        while url:
            res = requests.get(url, headers=headers, timeout=20)
            res.raise_for_status()

            data = res.json()
            all_preds.extend(data.get("results", []))
            url = data.get("next")

    except requests.RequestException as e:
        print(f"Erro API: {e}")
        return []

    print(f"Total predictions coletadas: {len(all_preds)}")
    return all_preds


def get_matches():
    predictions = get_predictions()
    bets = []

    for p in predictions:
        try:
            event = p["event"]
            confidence = float(p.get("confidence", 0))

            if confidence < 0.55:
                continue

            teams = f"{event['home_team']} vs {event['away_team']}"

            prob_over_25 = p.get("prob_over_25")
            if prob_over_25 is not None and prob_over_25 > 55:
                bets.append({
                    "type": "over_2.5",
                    "prob": prob_over_25 / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event.get("event_date"),
                })

            prob_btts_yes = p.get("prob_btts_yes")
            if prob_btts_yes is not None and prob_btts_yes > 55:
                bets.append({
                    "type": "btts",
                    "prob": prob_btts_yes / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event.get("event_date"),
                })

        except (KeyError, TypeError, ValueError):
            continue

    print(f"Total bets geradas: {len(bets)}")
    return bets
