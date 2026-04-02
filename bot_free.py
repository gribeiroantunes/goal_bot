import os
from main import run
from data_collector import get_matches
from telegram import Bot


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_FREE")


def format_bet_message(bet):
    return (
        f"📊 Oportunidade FREE\n\n"
        f"➡️ Tipo: {bet['type'].upper()}\n"
        f"📈 Probabilidade: {bet['prob']:.2%}\n"
        f"💰 Odds estimadas: {bet['odds']}\n"
        f"📊 EV: {bet['ev']:.2f}\n"
    )


def send_telegram(messages):
    bot = Bot(token=TOKEN)

    for msg in messages:
        bot.send_message(chat_id=CHAT_ID, text=msg)


def main():
    print("🔎 Coletando jogos...")
    matches = get_matches()

    if not matches:
        print("⚠️ Nenhum jogo encontrado.")
        return

    print("🧠 Processando modelo...")
    free, _ = run(matches)

    if not free:
        print("⚠️ Nenhuma oportunidade FREE encontrada.")
        return

    print(f"📤 Enviando {len(free)} apostas FREE...")

    messages = [format_bet_message(bet) for bet in free]

    send_telegram(messages)

    print("✅ BOT FREE finalizado com sucesso!")


if __name__ == "__main__":
    main()
