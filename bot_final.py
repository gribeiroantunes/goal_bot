# bot_final.py — Versão Final
import logging
from data_collector import get_events_week, get_predictions, merge_events_predictions
from market_analyzer import analyze_and_select

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s — %(message)s"
)
logger = logging.getLogger("overunder_bot")

def main(bankroll: float = 1000.0, top_n: int = 10):
    logger.info("="*60)
    logger.info("OVER/UNDER BOT REAL — RUN")
    logger.info("="*60)

    # Coleta dados
    events = get_events_week()
    logger.info(f"Eventos válidos coletados da API: {len(events)}")

    preds = get_predictions()
    logger.info(f"Previsões coletadas: {len(preds)} jogos")

    merged = merge_events_predictions(events, preds)
    logger.info(f"Eventos processados com forecasts: {len(merged)}")

    if not merged:
        logger.info("Nenhuma oportunidade hoje.")
        return

    # Seleção de apostas
    selections = analyze_and_select(merged)
    logger.info(f"Oportunidades filtradas: {len(selections)}")

    # Filtrar apenas apostas com confiança >= 50%
    selections = [b for b in selections if b["confidence"] >= 50]

    if not selections:
        logger.info("Nenhuma oportunidade com confiança >= 50% hoje.")
        return

    # Ordenar por probabilidade do modelo
    selections.sort(key=lambda x: x["model_prob"], reverse=True)

    # Escalar stakes proporcionalmente à confiança
    total_conf = sum(b["confidence"] for b in selections)
    for bet in selections:
        bet["stake"] = round(bankroll * bet["confidence"] / total_conf, 2)

    # Exposição total diária
    total_stake = sum(b["stake"] for b in selections)
    logger.info("Exposição diária total: %.2f%% do bankroll", total_stake / bankroll * 100)

    # Exibir top apostas
    logger.info("==== Oportunidades do dia (Top %d) ====", top_n)
    for bet in selections[:top_n]:
        logger.info(
            "JOGO | %s | Mercado: %s | Prob(Mod): %.2f | Conf: %.2f | Stake: %.2f",
            bet["fixture_name"], bet["market"],
            bet["model_prob"], bet["confidence"], bet["stake"]
        )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bankroll", type=float, default=1000)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    main(args.bankroll, args.top)