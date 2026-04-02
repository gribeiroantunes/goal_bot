MIN_PROB = 0.60
MIN_EV = 0.05


def filter_bets(value_data):
    approved = []

    for side in ["over", "under"]:
        data = value_data[side]

        if data["prob"] >= MIN_PROB and data["ev"] >= MIN_EV:
            approved.append({
                "type": side,
                **data
            })

    return approved
