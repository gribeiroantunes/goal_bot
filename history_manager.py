# history_manager.py

import json
import os
from datetime import datetime
from config import HISTORY_FILE


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_bet(entry):
    data = load_history()

    if any(x["game_id"] == entry["game_id"] for x in data):
        return

    data.append(entry)
    save_history(data)


def update_result(game_id, result):
    data = load_history()

    for bet in data:
        if bet["game_id"] == game_id:
            bet["result"] = result

    save_history(data)


def create_bet_entry(game):
    return {
        "game_id": game["id"],
        "league": game["league"],
        "market": game["market"],
        "prob": game["prob"],
        "ev": game["ev"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "result": "pending"
    }
