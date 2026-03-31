import json
from datetime import datetime

FILE = "historico_apostas.json"


def save_bet(bet):
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    bet["timestamp"] = datetime.now().isoformat()
    data.append(bet)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def analyze():
    with open(FILE, "r") as f:
        data = json.load(f)

    total = len(data)
    wins = sum(1 for d in data if d.get("result") == "win")

    print(f"Total: {total}")
    print(f"Winrate: {wins/total:.2%}")