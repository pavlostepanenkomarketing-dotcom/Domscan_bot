import os
from telegram.ext import Updater, CommandHandler
from evaluator import load_domains

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_FILE = "chat_id.txt"


def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))


def get_chat_id():
    if not os.path.exists(CHAT_ID_FILE):
        return None
    return int(open(CHAT_ID_FILE).read().strip())


def start(update, context):
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)
    update.message.reply_text(
        "Привет! Я Domscan бот 🔍\n"
        "Буду находить домены дороже 20 000 €.\n"
        "Команда /today покажет лучшие домены."
    )


def today(update, context):
    results = load_domains()
    if not results:
        update.message.reply_text("Сегодня премиальных доменов нет.")
        return

    txt = "🔥 Домены дороже 20 000 €:\n\n"
    for d in results[:20]:
        txt += f"{d['domain']} – ~{d['price']:,} € (ACR {d['acr']})\n"

    update.message.reply_text(txt)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
