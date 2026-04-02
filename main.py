from stat_model_goals import analyze_match
from value_analyzer import analyze_value
from filters import filter_bets
from ranking import split_free_vip


def process_match(home, away, league="default"):
    model = analyze_match(home, away, league)

    value = analyze_value(
        model["prob_over"],
        model["prob_under"]
    )

    bets = filter_bets(value)

    return bets


def run(matches):
    all_bets = []

    for match in matches:
        bets = process_match(match["home"], match["away"], match["league"])
        all_bets.extend(bets)

    free, vip = split_free_vip(all_bets)

    return free, vip
