"""
backtester.py
=============
Módulo de Backtesting para o Corner Betting Bot.

Responsável por:
- Simular o desempenho do modelo em dados históricos
- Realizar simulações de Monte Carlo para avaliar variância e risco de ruína
- Calcular métricas de performance (ROI, Yield, Sharpe Ratio, Max Drawdown)
- Validar a eficácia dos filtros de precisão e otimização de CLV
"""

import json
import logging
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import asdict
from typing import List, Dict, Optional

from statistical_model import BetRecommendation, MatchPrediction
from market_analyzer import BankrollState, apply_bet_result

logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, initial_bankroll: float = 1000.0):
        self.initial_bankroll = initial_bankroll
        self.bankroll_state = BankrollState(
            initial_bankroll=initial_bankroll,
            current_bankroll=initial_bankroll,
            peak_bankroll=initial_bankroll
        )
        self.results = []

    def run_backtest(self, historical_data: List[Dict]):
        """
        Executa o backtest em uma lista de dados históricos.
        Cada item em historical_data deve conter a recomendação e o resultado real.
        """
        logger.info(f"Iniciando backtest em {len(historical_data)} registros...")
        
        for entry in historical_data:
            rec_dict = entry.get("recommendation")
            actual_corners = entry.get("actual_corners")
            
            if not rec_dict or actual_corners is None:
                continue
                
            rec = BetRecommendation(**rec_dict)
            
            # Determinar se a aposta ganhou
            # Ex: "Over 9.5 Escanteios" -> side="over", line=9.5
            market_parts = rec.market.split()
            side = market_parts[0].lower()
            line = float(market_parts[1])
            
            won = False
            if side == "over" and actual_corners > line:
                won = True
            elif side == "under" and actual_corners < line:
                won = True
                
            # Aplicar resultado na banca
            stake_abs = rec.stake_pct * self.bankroll_state.current_bankroll
            apply_bet_result(self.bankroll_state, stake_abs, won, rec.odd)
            
            # Registrar resultado
            self.results.append({
                "fixture_id": rec.fixture_id,
                "market": rec.market,
                "odd": rec.odd,
                "won": won,
                "stake_pct": rec.stake_pct,
                "bankroll_after": self.bankroll_state.current_bankroll,
                "ev_pct": rec.ev_pct,
                "clv_estimate": rec.clv_estimate
            })

    def run_monte_carlo(self, num_simulations: int = 1000, num_bets: int = 100):
        """
        Realiza simulação de Monte Carlo baseada nos resultados do backtest
        ou em parâmetros estatísticos médios do modelo.
        """
        if not self.results:
            logger.warning("Nenhum resultado de backtest disponível para Monte Carlo. Usando parâmetros padrão.")
            # Simulação baseada em parâmetros hipotéticos (ex: 55% win rate em odds 2.0)
            avg_win_rate = 0.53
            avg_odd = 2.0
            avg_stake = 0.02
        else:
            df = pd.DataFrame(self.results)
            avg_win_rate = df["won"].mean()
            avg_odd = df["odd"].mean()
            avg_stake = df["stake_pct"].mean()

        sim_results = []
        for _ in range(num_simulations):
            current_bankroll = self.initial_bankroll
            bankroll_history = [current_bankroll]
            
            for _ in range(num_bets):
                stake = current_bankroll * avg_stake
                if random.random() < avg_win_rate:
                    current_bankroll += stake * (avg_odd - 1)
                else:
                    current_bankroll -= stake
                
                bankroll_history.append(current_bankroll)
                if current_bankroll <= 0:
                    break
            
            sim_results.append(bankroll_history)
            
        return sim_results

    def get_metrics(self) -> Dict:
        """Calcula métricas de desempenho do backtest."""
        if not self.results:
            return {}
            
        df = pd.DataFrame(self.results)
        total_bets = len(df)
        win_rate = df["won"].mean()
        
        # ROI = Lucro Total / Valor Total Apostado
        total_staked = (df["stake_pct"] * df["bankroll_after"].shift(1).fillna(self.initial_bankroll)).sum()
        total_profit = self.bankroll_state.current_bankroll - self.initial_bankroll
        roi = total_profit / total_staked if total_staked > 0 else 0
        
        # Yield = ROI por aposta
        yield_pct = roi # Simplificação, geralmente yield e ROI são usados de forma intercambiável em apostas
        
        # Sharpe Ratio (simplificado para apostas)
        returns = df["bankroll_after"].pct_change().dropna()
        sharpe = (returns.mean() / returns.std() * np.sqrt(total_bets)) if returns.std() > 0 else 0
        
        return {
            "total_bets": total_bets,
            "win_rate": round(win_rate, 4),
            "total_profit": round(total_profit, 2),
            "roi_pct": round(roi * 100, 2),
            "sharpe_ratio": round(sharpe, 2),
            "max_drawdown_pct": round(self.bankroll_state.current_drawdown * 100, 2),
            "final_bankroll": round(self.bankroll_state.current_bankroll, 2)
        }

def generate_historical_mock_data(num_records: int = 50) -> List[Dict]:
    """Gera dados históricos fictícios para demonstrar o backtester."""
    data = []
    for i in range(num_records):
        odd = round(random.uniform(1.7, 2.3), 2)
        prob_est = round(1.0 / odd + random.uniform(0.02, 0.1), 4) # Edge positivo simulado
        ev = (prob_est * odd) - 1
        
        rec = {
            "fixture_id": 2000 + i,
            "home_team": f"Team H{i}",
            "away_team": f"Team A{i}",
            "league": "Mock League",
            "market": "Over 9.5 Escanteios" if random.random() > 0.5 else "Under 10.5 Escanteios",
            "bookmaker": "Pinnacle",
            "odd": odd,
            "prob_estimated": prob_est,
            "prob_implied": round(1.0/odd, 4),
            "ev_pct": ev,
            "kelly_fraction": round(ev / (odd - 1) * 0.25, 4),
            "stake_pct": round(min(0.03, ev / (odd - 1) * 0.05), 4),
            "confidence": "media",
            "confidence_score": random.uniform(50, 80),
            "clv_estimate": ev * 0.5
        }
        
        # Resultado real (simulando variância)
        actual_corners = random.randint(5, 15)
        
        data.append({
            "recommendation": rec,
            "actual_corners": actual_corners
        })
    return data

if __name__ == "__main__":
    # Exemplo de uso
    logging.basicConfig(level=logging.INFO)
    bt = Backtester(initial_bankroll=1000.0)
    mock_data = generate_historical_mock_data(100)
    bt.run_backtest(mock_data)
    metrics = bt.get_metrics()
    print("Métricas do Backtest:")
    print(json.dumps(metrics, indent=2))
    
    # Monte Carlo
    sims = bt.run_monte_carlo(num_simulations=100, num_bets=50)
    print(f"Simulações de Monte Carlo concluídas: {len(sims)}")
