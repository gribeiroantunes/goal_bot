import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Bot
from config import TELEGRAM_CHAT_ID_VIP as CHAT_ID

TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = ZoneInfo("America/Sao_Paulo")


def format_market(market):
    mapping = {
        "over_1.5": "Mais de 1.5 gols",
        "over_2.5": "Mais de 2.5 gols",
        "over_3.5": "Mais de 3.5 gols",
        "under_1.5": "Menos de 1.5 gols",
        "under_2.5": "Menos de 2.5 gols",
        "under_3.5": "Menos de 3.5 gols",
        "btts": "Ambas marcam",
        "no_btts": "Ambas não marcam",
        "home_win": "Time da casa vence",
        "draw": "Empate",
        "away_win": "Time visitante vence",
    }
    return mapping.get(market, market.replace("_", " ").title())


def stake_percentage(prob, confidence):
    edge = max((prob * confidence) - 0.50, 0)
    stake = 0.75 + (edge / 0.50) * 2.75
    return max(0.75, min(3.5, round(stake, 2)))


def format_date_time(event_date):
    if not event_date:
        return "N/A", "N/A"

    try:
        dt = datetime.fromisoformat(event_date.replace("Z", "+00:00")).astimezone(TZ)
        return dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M")
    except Exception:
        return "N/A", "N/A"


def format_msg(bet):
    date_str, time_str = format_date_time(bet.get("event_date"))
    return (
        f"🔥 TIP VIP\n\n"
        f"Jogo: {bet.get('teams', 'N/A')}\n"
        f"Data: {date_str}\n"
        f"Hora: {time_str}\n"
        f"Mercado: {format_market(bet.get('type', 'N/A'))}\n"
        f"Probabilidade: {bet.get('prob', 0):.2%}\n"
        f"Confiança da análise: {bet.get('confidence', 0):.2f}\n"
        f"Stake sugerida: {stake_percentage(bet.get('prob', 0), bet.get('confidence', 0)):.2f}% da banca"
    )


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN não encontrado no ambiente")
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID_VIP não encontrado no config")

    from main import run

    _, vip = run()
    bot = Bot(token=TOKEN)

    bot.send_message(chat_id=CHAT_ID, text="🔥 MELHORES OPORTUNIDADES (VIP)\n")

    if not vip:
        bot.send_message(chat_id=CHAT_ID, text="Nenhuma tip vip encontrada hoje.")
        return

    for bet in vip:
        try:
            bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")


if __name__ == "__main__":
    main()
