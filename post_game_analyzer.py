# post_game_analyzer.py

from history_manager import load_history, update_result


def settle(results):
    history = load_history()

    for bet in history:
        if bet["result"] != "pending":
            continue

        game_id = bet["game_id"]

        if game_id in results:
            update_result(game_id, results[game_id])
