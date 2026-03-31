"""
report_generator.py
===================
Módulo de geração de relatórios do Corner Betting Bot.

Responsável por:
- Formatar e exibir o bilhete diário de apostas
- Gerar relatório em texto, JSON e Markdown
- Registrar histórico completo de apostas em log
- Exibir resumo de desempenho da banca
"""

import json
import logging
import os
from dataclasses import asdict
from datetime import date, datetime
from typing import Optional

from statistical_model import BetRecommendation
from market_analyzer import BankrollState

logger = logging.getLogger(__name__)

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "bet_history.json")
REPORT_DIR   = os.path.join(os.path.dirname(__file__), "reports")


# ---------------------------------------------------------------------------
# Formatação do bilhete
# ---------------------------------------------------------------------------

CONFIDENCE_LABELS = {
    "alta":  "🟢 ALTA",
    "media": "🟡 MÉDIA",
    "baixa": "🔴 BAIXA",
}

CONFIDENCE_LABELS_PLAIN = {
    "alta":  "[ALTA]",
    "media": "[MEDIA]",
    "baixa": "[BAIXA]",
}


def format_ticket(bets: list[BetRecommendation],
                  bankroll_state: BankrollState,
                  date_str: Optional[str] = None) -> str:
    """
    Formata o bilhete diário de apostas em texto legível.

    Parâmetros
    ----------
    bets           : lista de apostas recomendadas (ordenadas por score)
    bankroll_state : estado atual da banca
    date_str       : data do bilhete (padrão: hoje)

    Retorno
    -------
    str : bilhete formatado
    """
    if date_str is None:
        date_str = date.today().strftime("%d/%m/%Y")

    lines = []
    lines.append("=" * 70)
    lines.append(f"  CORNER BETTING BOT — BILHETE DIÁRIO DE APOSTAS")
    lines.append(f"  Data: {date_str}  |  Gerado em: {datetime.utcnow().strftime('%H:%M UTC')}")
    lines.append("=" * 70)
    lines.append(f"  Banca Atual: R$ {bankroll_state.current_bankroll:,.2f}  |  "
                 f"Drawdown: {bankroll_state.current_drawdown:.1%}  |  "
                 f"Exposição Diária: {bankroll_state.daily_exposure:.1%}")
    lines.append("=" * 70)

    if not bets:
        lines.append("")
        lines.append("  ⚠  Nenhuma aposta com valor identificada hoje.")
        lines.append("")
        lines.append("  O sistema analisou todos os jogos disponíveis e não encontrou")
        lines.append("  oportunidades com EV ≥ +5% e qualidade suficiente.")
        lines.append("")
        lines.append("=" * 70)
        return "\n".join(lines)

    total_stake = sum(b.stake_pct for b in bets)
    lines.append(f"  Total de apostas: {len(bets)}  |  Exposição total: {total_stake:.1%}")
    lines.append("=" * 70)
    lines.append("")

    for i, bet in enumerate(bets, 1):
        conf_label = CONFIDENCE_LABELS_PLAIN.get(bet.confidence, bet.confidence.upper())
        lines.append(f"  APOSTA #{i}  {conf_label}  (Score: {bet.confidence_score:.0f}/100)")
        lines.append(f"  {'─' * 60}")
        lines.append(f"  Jogo:         {bet.home_team} vs {bet.away_team}")
        lines.append(f"  Liga:         {bet.league}")
        lines.append(f"  Mercado:      {bet.market}")
        lines.append(f"  Casa:         {bet.bookmaker}")
        lines.append(f"  Odd:          {bet.odd:.2f}")
        lines.append(f"  Prob. Est.:   {bet.prob_estimated:.1%}  |  "
                     f"Prob. Impl.: {bet.prob_implied:.1%}")
        lines.append(f"  EV:           +{bet.ev_pct:.1%}")
        lines.append(f"  Kelly Frac.:  {bet.kelly_fraction:.2%}")
        lines.append(f"  Stake:        {bet.stake_pct:.2%} da banca  "
                     f"(R$ {bet.stake_pct * bankroll_state.current_bankroll:,.2f})")
        lines.append(f"  CLV Est.:     +{bet.clv_estimate:.1%}")
        lines.append("")

    lines.append("=" * 70)
    lines.append("  RESUMO FINANCEIRO")
    lines.append(f"  {'─' * 60}")
    lines.append(f"  Apostas recomendadas:  {len(bets)}")
    lines.append(f"  Exposição total:       {total_stake:.2%}")
    lines.append(f"  Valor total apostado:  R$ {total_stake * bankroll_state.current_bankroll:,.2f}")
    lines.append(f"  EV médio:              +{sum(b.ev_pct for b in bets) / len(bets):.1%}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("  AVISO: Este sistema é uma ferramenta de análise quantitativa.")
    lines.append("  Apostas envolvem risco. Aposte com responsabilidade.")
    lines.append("=" * 70)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Geração de relatório Markdown
# ---------------------------------------------------------------------------

def generate_markdown_report(bets: list[BetRecommendation],
                              bankroll_state: BankrollState,
                              date_str: Optional[str] = None) -> str:
    """
    Gera relatório completo em formato Markdown.
    """
    if date_str is None:
        date_str = date.today().strftime("%d/%m/%Y")

    md = []
    md.append(f"# Corner Betting Bot — Relatório Diário")
    md.append(f"**Data:** {date_str} | **Gerado em:** {datetime.utcnow().strftime('%H:%M UTC')}")
    md.append("")

    # Resumo da banca
    md.append("## Estado da Banca")
    md.append("")
    md.append("| Métrica | Valor |")
    md.append("|---|---|")
    md.append(f"| Banca Atual | R$ {bankroll_state.current_bankroll:,.2f} |")
    md.append(f"| Banca Inicial | R$ {bankroll_state.initial_bankroll:,.2f} |")
    md.append(f"| Pico da Banca | R$ {bankroll_state.peak_bankroll:,.2f} |")
    md.append(f"| Drawdown Atual | {bankroll_state.current_drawdown:.1%} |")
    md.append(f"| Exposição Diária | {bankroll_state.daily_exposure:.1%} |")
    md.append(f"| Total de Apostas | {bankroll_state.total_bets} |")
    if bankroll_state.total_bets > 0:
        win_rate = bankroll_state.total_wins / bankroll_state.total_bets
        md.append(f"| Taxa de Acerto | {win_rate:.1%} |")
    md.append("")

    if not bets:
        md.append("## Apostas do Dia")
        md.append("")
        md.append("> **Nenhuma aposta com valor identificada hoje.**")
        md.append(">")
        md.append("> O sistema analisou todos os jogos disponíveis e não encontrou "
                  "oportunidades com EV ≥ +5% e qualidade suficiente.")
        md.append("")
        return "\n".join(md)

    md.append("## Apostas Recomendadas")
    md.append("")
    md.append("| # | Jogo | Liga | Mercado | Casa | Odd | Prob. Est. | EV | Stake | Confiança |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")

    for i, bet in enumerate(bets, 1):
        conf_label = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}.get(bet.confidence, "—")
        md.append(
            f"| {i} | {bet.home_team} vs {bet.away_team} | {bet.league} | "
            f"{bet.market} | {bet.bookmaker} | {bet.odd:.2f} | "
            f"{bet.prob_estimated:.1%} | +{bet.ev_pct:.1%} | "
            f"{bet.stake_pct:.2%} | {conf_label} |"
        )

    md.append("")
    md.append("## Detalhamento das Apostas")
    md.append("")

    for i, bet in enumerate(bets, 1):
        conf_label = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}.get(bet.confidence, "—")
        md.append(f"### Aposta #{i} — {bet.home_team} vs {bet.away_team}")
        md.append("")
        md.append(f"**Liga:** {bet.league}  ")
        md.append(f"**Mercado:** {bet.market}  ")
        md.append(f"**Casa de Apostas:** {bet.bookmaker}  ")
        md.append("")
        md.append("| Métrica | Valor |")
        md.append("|---|---|")
        md.append(f"| Odd Oferecida | {bet.odd:.3f} |")
        md.append(f"| Probabilidade Estimada | {bet.prob_estimated:.2%} |")
        md.append(f"| Probabilidade Implícita | {bet.prob_implied:.2%} |")
        md.append(f"| Valor Esperado (EV) | +{bet.ev_pct:.2%} |")
        md.append(f"| Kelly Fracionado | {bet.kelly_fraction:.3%} |")
        md.append(f"| Stake Recomendado | {bet.stake_pct:.3%} da banca |")
        md.append(f"| Valor em R$ | R$ {bet.stake_pct * bankroll_state.current_bankroll:,.2f} |")
        md.append(f"| CLV Estimado | +{bet.clv_estimate:.2%} |")
        md.append(f"| Nível de Confiança | {conf_label} |")
        md.append(f"| Score do Modelo | {bet.confidence_score:.0f}/100 |")
        md.append("")

    # Resumo financeiro
    total_stake = sum(b.stake_pct for b in bets)
    avg_ev      = sum(b.ev_pct for b in bets) / len(bets)

    md.append("## Resumo Financeiro")
    md.append("")
    md.append("| Métrica | Valor |")
    md.append("|---|---|")
    md.append(f"| Apostas Recomendadas | {len(bets)} |")
    md.append(f"| Exposição Total | {total_stake:.2%} |")
    md.append(f"| Valor Total Apostado | R$ {total_stake * bankroll_state.current_bankroll:,.2f} |")
    md.append(f"| EV Médio | +{avg_ev:.2%} |")
    md.append("")
    md.append("---")
    md.append("*Este sistema é uma ferramenta de análise quantitativa. "
              "Apostas envolvem risco. Aposte com responsabilidade.*")

    return "\n".join(md)


# ---------------------------------------------------------------------------
# Persistência de histórico
# ---------------------------------------------------------------------------

def save_bet_to_history(bet: BetRecommendation, date_str: Optional[str] = None):
    """Registra aposta no histórico persistente."""
    if date_str is None:
        date_str = date.today().isoformat()

    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    entry = asdict(bet)
    entry["date"]   = date_str
    entry["result"] = "pending"   # será atualizado após o jogo
    entry["profit"] = None
    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def update_bet_result(fixture_id: int, market: str,
                      won: bool, closing_odd: Optional[float] = None):
    """
    Atualiza resultado de uma aposta no histórico.
    Calcula CLV real se odd de fechamento for fornecida.
    """
    if not os.path.exists(HISTORY_FILE):
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    for entry in history:
        if entry.get("fixture_id") == fixture_id and entry.get("market") == market:
            if entry.get("result") == "pending":
                entry["result"]       = "win" if won else "loss"
                entry["closing_odd"]  = closing_odd
                if closing_odd:
                    # CLV real = (odd_apostada / odd_fechamento) - 1
                    entry["clv_real"] = round(entry["odd"] / closing_odd - 1.0, 4)
                break

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def save_report_to_file(content: str, fmt: str = "txt") -> str:
    """
    Salva relatório em arquivo e retorna o caminho.

    Parâmetros
    ----------
    fmt : "txt" | "md" | "json"
    """
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"report_{date.today().isoformat()}.{fmt}"
    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Relatório salvo em: %s", filepath)
    return filepath


def generate_json_report(bets: list[BetRecommendation],
                          bankroll_state: BankrollState) -> dict:
    """Gera relatório em formato JSON estruturado."""
    return {
        "date":      date.today().isoformat(),
        "generated": datetime.utcnow().isoformat(),
        "bankroll": {
            "current":       bankroll_state.current_bankroll,
            "initial":       bankroll_state.initial_bankroll,
            "peak":          bankroll_state.peak_bankroll,
            "drawdown_pct":  round(bankroll_state.current_drawdown * 100, 2),
            "daily_exposure_pct": round(bankroll_state.daily_exposure * 100, 2),
            "total_bets":    bankroll_state.total_bets,
            "total_wins":    bankroll_state.total_wins,
            "total_losses":  bankroll_state.total_losses,
        },
        "bets": [asdict(b) for b in bets],
        "summary": {
            "total_bets":      len(bets),
            "total_exposure":  round(sum(b.stake_pct for b in bets) * 100, 2),
            "avg_ev_pct":      round(sum(b.ev_pct for b in bets) / len(bets) * 100, 2) if bets else 0,
            "avg_confidence":  round(sum(b.confidence_score for b in bets) / len(bets), 1) if bets else 0,
        } if bets else {
            "total_bets": 0,
            "message": "Nenhuma aposta com valor identificada hoje",
        },
    }
