# =========================
# 📡 TELEGRAM CONFIG
# =========================

# IDs dos grupos (OBRIGATÓRIO)
TELEGRAM_CHAT_ID_FREE = -1003725207734
TELEGRAM_CHAT_ID_VIP = -1003858302105


# =========================
# ⚙️ MODELO ESTATÍSTICO
# =========================

# Média geral de gols (pode ajustar por liga futuramente)
LEAGUE_AVG_GOALS = 2.5

# Vantagem de jogar em casa
HOME_ADVANTAGE = 0.15

# Máximo de gols simulados no modelo
MAX_GOALS = 6


# =========================
# 💰 MERCADO / ODDS
# =========================

# Margem simulada da casa
BOOKMAKER_MARGIN = 0.08


# =========================
# 📊 RANKING E SELEÇÃO
# =========================

# Peso da probabilidade no score
WEIGHT_PROB = 0.6

# Peso do EV no score
WEIGHT_EV = 0.4

# Quantidade de picks
VIP_PICKS = 5
FREE_PICKS = 5


# =========================
# 🎯 ESTRATÉGIA
# =========================

# Sempre enviar mensagem mesmo sem aposta
ALWAYS_SEND_MESSAGE = True

# Mensagens padrão
MSG_NO_FREE = "⚠️ Hoje não encontramos grandes oportunidades.\nFique atento ao VIP 🔥"
MSG_NO_VIP = "⚠️ Mercado fraco hoje.\nEntradas reduzidas para proteção de banca."


# =========================
# 🔒 SEGURANÇA / DEBUG
# =========================

DEBUG_MODE = True


# =========================
# 📦 API CONFIG
# =========================

# Sua API (ajuste conforme necessário)
API_URL = "https://api.exemplo.com/matches"


# =========================
# 🧠 FUTURO (PRONTO PRA EXPANSÃO)
# =========================

# Controle de stake (ainda não usado, mas preparado)
DEFAULT_STAKE_PERCENT = 0.05

# Controle de risco
MAX_DAILY_BETS = 10
