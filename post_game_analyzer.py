# post_game_analyzer.py

from history_manager import load_history, update_result


def get_results():
    # ⚠️ SUBSTITUIR pela sua API real
    return {
        "1": "win"
    }


def main():
    results = get_results()
    history = load_history()

    for bet in history:
        if bet["result"] != "pending":
            continue

        game_id = bet["game_id"]

        if game_id in results:
            update_result(game_id, results[game_id])


if __name__ == "__main__":
    main()
