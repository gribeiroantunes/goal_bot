import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Bot
from config import TELEGRAM_CHAT_ID_FREE as CHAT_ID

TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = ZoneInfo("America/Sao_Paulo")


def format_market(market):
    mapping = {
        "over_1.5": "Mais de 1.5 gols",
        "over_2.5": "Mais de 2.5 gols",
        "under_2.5": "Menos de 2.5 gols",
        "btts": "Ambas marcam",
        "no_btts": "Ambas não marcam",
    }
    return mapping.get(market, market.replace("_", " ").title())


def stake_percentage(prob, confidence):
    edge = max((prob * confidence) - 0.50, 0)
    stake = 0.5 + (edge / 0.50) * 2.0
    return max(0.5, min(2.5, round(stake, 2)))


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
        f"📊 TIP FREE\n\n"
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
        raise ValueError("TELEGRAM_CHAT_ID_FREE não encontrado no config")

    from main import run

    free, _ = run()
    bot = Bot(token=TOKEN)

    bot.send_message(chat_id=CHAT_ID, text="📊 OPORTUNIDADES DO DIA (FREE)\n")

    if not free:
        bot.send_message(chat_id=CHAT_ID, text="Nenhuma tip free encontrada hoje.")
        return

    for bet in free:
        try:
            bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")


if __name__ == "__main__":
    main()
