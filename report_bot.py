import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Bot

# ================= CONFIG =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 🔥 SEU CANAL FREE (já configurado)
CHANNEL_ID = -1003725207734

# 🔗 SEU LINK VIP (já inserido)
VIP_LINK = "https://t.me/+ckOVtoDxOItmMzUx"

HISTORY_FILE = "history.json"
# ==========================================


# --------- CARREGAR HISTÓRICO ---------
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# --------- FILTRAR ÚLTIMOS 7 DIAS ---------
def get_last_7_days(data):
    cutoff = datetime.now() - timedelta(days=7)

    result = []
    for item in data:
        try:
            date = datetime.strptime(item["date"], "%Y-%m-%d")
            if date >= cutoff:
                result.append(item)
        except:
            continue

    return result


# --------- CALCULAR ESTATÍSTICAS ---------
def calculate_stats(data):
    wins = sum(1 for x in data if x.get("result") == "win")
    losses = sum(1 for x in data if x.get("result") == "loss")

    total = wins + losses
    accuracy = (wins / total * 100) if total > 0 else 0

    return wins, losses, accuracy


# --------- FORMATAR MENSAGEM ---------
def format_message(wins, losses, acc):
    return (
        f"📊 *RESULTADOS DOS ÚLTIMOS 7 DIAS*\n\n"
        f"✅ *Wins:* {wins}\n"
        f"❌ *Losses:* {losses}\n"
        f"📈 *Assertividade:* {acc:.1f}%\n\n"
        f"🔥 Método baseado em análise estatística\n"
        f"📊 Foco em consistência e longo prazo\n\n"
        f"💎 *GRUPO VIP DE SINAIS*\n"
        f"✔ Entradas com alta probabilidade\n"
        f"✔ Mercados: Gols + Resultado (1X2)\n"
        f"✔ Gestão profissional (5% a 7%)\n\n"
        f"🚀 *Entre agora:*\n{VIP_LINK}"
    )


# --------- MAIN ---------
async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    history = load_history()
    recent = get_last_7_days(history)

    wins, losses, acc = calculate_stats(recent)

    message = format_message(wins, losses, acc)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    asyncio.run(main())