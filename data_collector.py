import requests
import os

API_KEY = os.getenv("BZ_API_KEY")
BASE_URL = "https://api.sports.bzzoiro.com"


def get_last_matches(team_id):
    url = f"{BASE_URL}/team/{team_id}/matches"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
    except:
        return []

    return data.get("matches", [])[:5]  # últimos 5 jogos


def calculate_team_stats(matches):
    goals_for = 0
    goals_against = 0
    total = len(matches)

    if total == 0:
        return 1.2, 1.2  # fallback

    for m in matches:
        try:
            goals_for += m["goals_for"]
            goals_against += m["goals_against"]
        except:
            continue

    return goals_for / total, goals_against / total


def get_matches():
    url = f"{BASE_URL}/matches/today"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
    except:
        return []

    matches = []

    for game in data.get("matches", []):
        try:
            home_id = game["home_id"]
            away_id = game["away_id"]

            home_last = get_last_matches(home_id)
            away_last = get_last_matches(away_id)

            home_for, home_against = calculate_team_stats(home_last)
            away_for, away_against = calculate_team_stats(away_last)

            matches.append({
                "home": {
                    "avg_goals_scored": home_for,
                    "avg_goals_conceded": home_against
                },
                "away": {
                    "avg_goals_scored": away_for,
                    "avg_goals_conceded": away_against
                }
            })

        except:
            continue

    return matches
