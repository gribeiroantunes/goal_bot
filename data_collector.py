import requests
import os

API_KEY = os.getenv("BZ_API_KEY")
BASE_URL = "https://sports.bzzoiro.com/api"


def get_predictions():
    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    all_preds = []
    url = f"{BASE_URL}/predictions/?tz=America/Sao_Paulo"

    try:
        while url:
            res = requests.get(url, headers=headers)
            data = res.json()

            results = data.get("results", [])
            all_preds.extend(results)

            url = data.get("next")  # 🔥 pega próxima página

    except Exception as e:
        print(f"Erro API: {e}")

    print(f"Total predictions coletadas: {len(all_preds)}")
    return all_preds
