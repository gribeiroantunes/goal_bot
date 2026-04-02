def filter_bets(value_data):
    bets = []

    for side in ["over", "under"]:
        bets.append({
            "type": side,
            **value_data[side]
        })

    return bets
