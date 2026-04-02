import os
from main import run
from data_collector import get_matches
from telegram import Bot


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_VIP")


def format_bet_message(bet):
    return (
        f"🔥 OPORTUNIDADE VIP 🔥\n\n"
        f"➡️ Tipo: {bet['type'].upper()}\n"
        f"📈 Probabilidade: {bet['prob']:.2%}\n"
        f"💰 Odds estimadas: {bet['odds']}\n"
        f"📊 EV: {bet['ev']:.2f}\n"
        f"⭐ Score: {bet.get('score', 0):.4f}\n"
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
    _, vip = run(matches)

    if not vip:
        print("⚠️ Nenhuma oportunidade VIP encontrada.")
        return

    print(f"📤 Enviando {len(vip)} apostas VIP...")

    messages = [format_bet_message(bet) for bet in vip]

    send_telegram(messages)

    print("✅ BOT VIP finalizado com sucesso!")


if __name__ == "__main__":
    main()
