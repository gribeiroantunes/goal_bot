import requests

API_URL = "https://api.football-data-api.com/todays-matches"  # exemplo


def get_matches():
    """
    Retorna lista de jogos no formato padrão do modelo
    """

    try:
        response = requests.get(API_URL)
        data = response.json()
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []

    matches = []

    for game in data.get("data", []):
        try:
            home = {
                "avg_goals_scored": game["home_team"]["avg_goals_scored"],
                "avg_goals_conceded": game["home_team"]["avg_goals_conceded"]
            }

            away = {
                "avg_goals_scored": game["away_team"]["avg_goals_scored"],
                "avg_goals_conceded": game["away_team"]["avg_goals_conceded"]
            }

            league = game.get("league", "default")

            matches.append({
                "home": home,
                "away": away,
                "league": league
            })

        except KeyError:
            continue

    return matches
