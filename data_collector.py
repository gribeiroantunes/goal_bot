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

            market_map = [
                ("over_1.5", p.get("prob_over_15")),
                ("over_2.5", p.get("prob_over_25")),
                ("over_3.5", p.get("prob_over_35")),
                ("btts", p.get("prob_btts_yes")),
            ]

            for mtype, prob in market_map:
                if prob is not None and float(prob) > 55:
                    bets.append({
                        "type": mtype,
                        "prob": float(prob) / 100,
                        "confidence": confidence,
                        "teams": teams,
                        "event_date": event_date,
                    })

            under_candidates = []
            prob_over_15 = p.get("prob_over_15")
            prob_over_25 = p.get("prob_over_25")
            prob_over_35 = p.get("prob_over_35")

            if prob_over_15 is not None:
                under_candidates.append(("under_1.5", 100 - float(prob_over_15)))
            if prob_over_25 is not None:
                under_candidates.append(("under_2.5", 100 - float(prob_over_25)))
            if prob_over_35 is not None:
                under_candidates.append(("under_3.5", 100 - float(prob_over_35)))

            for mtype, prob in under_candidates:
                if prob > 55:
                    bets.append({
                        "type": mtype,
                        "prob": prob / 100,
                        "confidence": confidence,
                        "teams": teams,
                        "event_date": event_date,
                    })

            prob_btts_yes = p.get("prob_btts_yes")
            if prob_btts_yes is not None:
                no_btts_prob = 100 - float(prob_btts_yes)
                if no_btts_prob > 55:
                    bets.append({
                        "type": "no_btts",
                        "prob": no_btts_prob / 100,
                        "confidence": confidence,
                        "teams": teams,
                        "event_date": event_date,
                    })

            prob_home = p.get("prob_home_win")
            prob_draw = p.get("prob_draw")
            prob_away = p.get("prob_away_win")

            for mtype, prob in [
                ("home_win", prob_home),
                ("draw", prob_draw),
                ("away_win", prob_away),
            ]:
                if prob is not None and float(prob) > 55:
                    bets.append({
                        "type": mtype,
                        "prob": float(prob) / 100,
                        "confidence": confidence,
                        "teams": teams,
                        "event_date": event_date,
                    })

        except (KeyError, TypeError, ValueError):
            continue

    print(f"Total bets geradas: {len(bets)}")
    return bets
