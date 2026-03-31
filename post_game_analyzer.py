"""
post_game_analyzer.py
=====================
Módulo de análise pós-jogo e aprendizado contínuo do Corner Betting Bot.

Responsável por:
- Comparar o resultado real de escanteios com as predições do modelo
- Identificar se o erro foi por variância estatística ou falha de modelagem
- Avaliar se o mercado (odds sharp) estava mais preciso que o modelo
- Gerar insights para ajuste de parâmetros de ligas e times
"""

import logging
import json
import os
from datetime import datetime
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class PostGameAnalyzer:
    def __init__(self, history_file: str = "bet_history.json"):
        self.history_file = history_file
        self.learning_data_file = "learning_insights.json"

    def analyze_results(self, fixture_id: int, actual_corners: int):
        """
        Analisa o resultado de um jogo e compara com a aposta realizada.
        """
        if not os.path.exists(self.history_file):
            return

        with open(self.history_file, "r") as f:
            history = json.load(f)

        bets = [b for b in history if b.get("fixture_id") == fixture_id]
        if not bets:
            return

        insights = []
        for bet in bets:
            # Lógica de análise de erro
            market = bet.get("market", "")
            side = "over" if "Over" in market else "under"
            line = float(market.split(" ")[1])
            
            # 1. Verificando se a aposta foi ganha
            won = (actual_corners > line) if side == "over" else (actual_corners < line)
            
            # 2. Avaliando erro do modelo vs variância
            # Se o resultado real estiver muito longe do lambda_total, pode ser variância extrema
            # Se o mercado (sharp_line_odd) previu melhor, o modelo precisa de ajuste
            lambda_total = bet.get("lambda_total", 0.0)
            model_error = abs(actual_corners - lambda_total)
            
            # Categorização do erro
            if model_error <= 1.5:
                error_type = "model_accurate"
            elif model_error <= 3.0:
                error_type = "standard_variance"
            else:
                error_type = "modeling_failure_or_extreme_variance"

            insight = {
                "fixture_id": fixture_id,
                "market": market,
                "actual_corners": actual_corners,
                "lambda_total": lambda_total,
                "won": won,
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            insights.append(insight)
            logger.info(f"Análise Pós-Jogo ({fixture_id}): {error_type} | Ganhou: {won}")

        self._save_insights(insights)

    def _save_insights(self, new_insights: list):
        data = []
        if os.path.exists(self.learning_data_file):
            with open(self.learning_data_file, "r") as f:
                data = json.load(f)
        
        data.extend(new_insights)
        with open(self.learning_data_file, "w") as f:
            json.dump(data, f, indent=2)

def generate_learning_summary():
    """Gera um resumo do aprendizado contínuo para o usuário."""
    if not os.path.exists("learning_insights.json"):
        return "Nenhum dado de aprendizado disponível ainda."
    
    with open("learning_insights.json", "r") as f:
        data = json.load(f)
    
    total = len(data)
    wins = sum(1 for i in data if i["won"])
    accurate = sum(1 for i in data if i["error_type"] == "model_accurate")
    
    summary = f"""
    --- RESUMO DE APRENDIZADO CONTÍNUO ---
    Total de jogos analisados: {total}
    Taxa de acerto (Win Rate): {wins/total:.1%}
    Precisão do Modelo (Erro < 1.5): {accurate/total:.1%}
    """
    return summary
