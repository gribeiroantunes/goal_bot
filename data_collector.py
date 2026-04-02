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
            event_date = event.get("event_date")

            candidates = [
                ("over_1.5", p.get("prob_over_15")),
                ("over_2.5", p.get("prob_over_25")),
                ("over_3.5", p.get("prob_over_35")),
                ("btts", p.get("prob_btts_yes")),
                ("home_win", p.get("prob_home_win")),
                ("draw", p.get("prob_draw")),
                ("away_win", p.get("prob_away_win")),
            ]

            for mtype, prob in candidates:
                if prob is not None and float(prob) >= 58:
                    bets.append({
                        "type": mtype,
                        "prob": float(prob) / 100,
                        "confidence": confidence,
                        "teams": teams,
                        "event_date": event_date,
                    })

            prob_over_15 = p.get("prob_over_15")
            prob_over_25 = p.get("prob_over_25")
            prob_over_35 = p.get("prob_over_35")
            prob_btts_yes = p.get("prob_btts_yes")

            if prob_over_15 is not None and (100 - float(prob_over_15)) >= 58:
                bets.append({
                    "type": "under_1.5",
                    "prob": (100 - float(prob_over_15)) / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event_date,
                })

            if prob_over_25 is not None and (100 - float(prob_over_25)) >= 58:
                bets.append({
                    "type": "under_2.5",
                    "prob": (100 - float(prob_over_25)) / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event_date,
                })

            if prob_over_35 is not None and (100 - float(prob_over_35)) >= 58:
                bets.append({
                    "type": "under_3.5",
                    "prob": (100 - float(prob_over_35)) / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event_date,
                })

            if prob_btts_yes is not None and (100 - float(prob_btts_yes)) >= 58:
                bets.append({
                    "type": "no_btts",
                    "prob": (100 - float(prob_btts_yes)) / 100,
                    "confidence": confidence,
                    "teams": teams,
                    "event_date": event_date,
                })

        except (KeyError, TypeError, ValueError):
            continue

    print(f"Total bets geradas: {len(bets)}")
    return bets
