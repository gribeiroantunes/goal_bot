def filter_bets(value_data):
    bets = []

    for side in ["over", "under"]:
        data = value_data[side]

        bets.append({
            "type": side,
            **data
        })

    return bets
