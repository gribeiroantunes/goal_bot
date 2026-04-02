import requests
import os

API_KEY = os.getenv("BZ_API_KEY")
BASE_URL = "https://sports.bzzoiro.com/api"


def get_predictions():
    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    try:
        response = requests.get(f"{BASE_URL}/predictions/", headers=headers)
        data = response.json()
    except Exception as e:
        print(f"Erro API: {e}")
        return []

    return data.get("results", [])


def get_matches():
    predictions = get_predictions()

    bets = []

    for p in predictions:
        try:
            event = p["event"]

            # 🔥 OVER 2.5
            if p.get("prob_over_25"):
                bets.append({
                    "type": "over_2.5",
                    "prob": p["prob_over_25"] / 100,
                    "confidence": p["confidence"],
                    "teams": f"{event['home_team']} vs {event['away_team']}"
                })

            # 🔥 BTTS
            if p.get("prob_btts_yes"):
                bets.append({
                    "type": "btts",
                    "prob": p["prob_btts_yes"] / 100,
                    "confidence": p["confidence"],
                    "teams": f"{event['home_team']} vs {event['away_team']}"
                })

        except:
            continue

    return bets
