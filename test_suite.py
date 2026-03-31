"""
test_suite.py
=============
Suite de testes integrados para o Corner Betting Bot Refinado.

Valida:
- Refinamentos do modelo estatístico (confiança e variância)
- Módulo de Backtesting e Monte Carlo
- Otimização de CLV e monitoramento de Sharp Lines
"""

import logging
import json
import os
from bot import run
from backtester import Backtester, generate_historical_mock_data
from market_analyzer import load_bankroll
from post_game_analyzer import PostGameAnalyzer, generate_learning_summary

# Configurar logging para o teste
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("test_suite")

def run_integrated_test():
    logger.info("INICIANDO SUITE DE TESTES INTEGRADOS")
    
    # 1. Teste de Execução do Bot (Modo Demo)
    logger.info("\n--- TESTE 1: Execução do Bot (Modo Demo) ---")
    try:
        recommendations = run(demo=True, bankroll_initial=1000.0)
        logger.info(f"Bot executado com sucesso. {len(recommendations)} recomendações geradas.")
        if recommendations:
            for r in recommendations:
                logger.info(f"Aposta: {r.market} | EV: {r.ev_pct:.1%} | Confiança: {r.confidence} | Score: {r.confidence_score}")
    except Exception as e:
        logger.error(f"Erro no Teste 1: {e}")

    # 2. Teste de Backtesting
    logger.info("\n--- TESTE 2: Módulo de Backtesting ---")
    try:
        bt = Backtester(initial_bankroll=1000.0)
        mock_data = generate_historical_mock_data(100)
        bt.run_backtest(mock_data)
        metrics = bt.get_metrics()
        logger.info("Métricas do Backtest (Simulado):")
        logger.info(json.dumps(metrics, indent=2))
    except Exception as e:
        logger.error(f"Erro no Teste 2: {e}")

    # 3. Teste de Monte Carlo
    logger.info("\n--- TESTE 3: Simulação de Monte Carlo ---")
    try:
        sims = bt.run_monte_carlo(num_simulations=1000, num_bets=100)
        final_values = [s[-1] for s in sims]
        ruin_count = sum(1 for v in final_values if v <= 0)
        logger.info(f"Simulações de Monte Carlo: 1000 execuções de 100 apostas cada.")
        logger.info(f"Banca Média Final: R$ {sum(final_values)/len(final_values):.2f}")
        logger.info(f"Risco de Ruína: {ruin_count/1000:.1%}")
    except Exception as e:
        logger.error(f"Erro no Teste 3: {e}")

    # 4. Teste de Aprendizado Contínuo (Post-Game)
    logger.info("\n--- TESTE 4: Análise Pós-Jogo e Aprendizado Contínuo ---")
    try:
        analyzer = PostGameAnalyzer()
        # Simulando resultados reais para os fixtures testados
        results = {1001: 8, 1002: 12, 1003: 10, 1004: 9, 1005: 11}
        for fid, res in results.items():
            analyzer.analyze_results(fid, res)
        
        summary = generate_learning_summary()
        logger.info(summary)
    except Exception as e:
        logger.error(f"Erro no Teste 4: {e}")

    logger.info("\nSUITE DE TESTES CONCLUÍDA")

if __name__ == "__main__":
    run_integrated_test()
