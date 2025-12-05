import os
import requests
from evaluator import load_domains

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_FILE = "chat_id.txt"


def get_chat_id():
    try:
        return int(open(CHAT_ID_FILE).read().strip())
    except:
        return None


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


def main():
    chat_id = get_chat_id()
    if not chat_id:
        print("Chat ID не найден — сначала сделай /start в Telegram боте.")
        return

    domains = load_domains()
    if not domains:
        send_message(chat_id, "Сегодня нет доменов дороже 20 000 €.")
        return

    msg = "🔥 Премиальные домены за сегодня:\n\n"
    for d in domains[:30]:
        msg += f"{d['domain']} – ~{d['price']:,} €\n"

    send_message(chat_id, msg)


if __name__ == "__main__":
    main()
