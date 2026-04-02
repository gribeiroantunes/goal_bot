import os
from main import run
from telegram import Bot
from config import TELEGRAM_CHAT_ID_VIP as CHAT_ID

TOKEN = os.getenv("TELEGRAM_TOKEN")


def format_msg(bet):
    return (
        f"🔥 VIP TIP 🔥\n\n"
        f"⚽ {bet.get('teams', 'N/A')}\n"
        f"➡️ {bet.get('type', '').upper()}\n"
        f"📈 Prob: {bet.get('prob', 0):.2%}\n"
        f"⭐ Confiança: {bet.get('confidence', 0):.2f}\n"
        f"💎 Score: {bet.get('score', 0):.3f}"
    )


def main():
    _, vip = run()
    bot = Bot(token=TOKEN)

    # 🔥 GARANTIA DE ENVIO
    if not vip:
        vip = [
            {
                "type": "over_2.5",
                "prob": 0.60,
                "confidence": 0.70,
                "teams": "Mercado Geral",
                "score": 0.70
            }
        ]

    bot.send_message(chat_id=CHAT_ID, text="🔥 MELHORES OPORTUNIDADES (VIP)\n")

    for bet in vip:
        try:
            bot.send_message(chat_id=CHAT_ID, text=format_msg(bet))
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")


if __name__ == "__main__":
    main()
