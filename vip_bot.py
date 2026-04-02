# vip_bot.py

from config import EV_MIN_VIP

def is_vip_bet(ev, score):
    return ev > EV_MIN_VIP and score > 0.70
