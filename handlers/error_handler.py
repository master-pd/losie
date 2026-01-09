# handlers/error_handler.py
from bot.instance import bot
from utils.logger import logger

@bot.errors_handler()
def error_handler(update, exception):
    logger.error(f"Telegram API Error: {exception}")
    if update:
        bot.send_message(update.chat.id, "😔 Something went wrong. Please try again later.")