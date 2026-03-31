#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from datetime import datetime
import requests
import os

TELEGRAM_TOKEN = os.environ.get("TG_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TG_CHAT_ID")

def save_csv(selections, filename="bets_history.csv"):
    """Salva apostas em CSV"""
    header = ["datetime", "fixture", "market", "odd", "ev", "stake_pct"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = [[now, s["fixture"], s["market"], s["odd"], s["ev"], s["stake_pct"]] for s in selections]

    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerows(rows)

def send_telegram_message(message):
    """Envia mensagem via Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Erro Telegram: {e}")

