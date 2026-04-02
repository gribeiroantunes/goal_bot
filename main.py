from stat_model_goals import analyze_match
from value_analyzer import analyze_value
from filters import filter_bets
from ranking import split_free_vip


def run(matches):
    all_bets = []

    for match in matches:
        model = analyze_match(match["home"], match["away"])

        value = analyze_value(
            model["prob_over"],
            model["prob_under"]
        )

        bets = filter_bets(value)

        all_bets.extend(bets)

    if not all_bets:
        return [], []

    free, vip = split_free_vip(all_bets)

    return free, vip
