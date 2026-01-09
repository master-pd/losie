# main.py - Bot entry point
from bot.instance import bot
from database.repository import init_db
from utils.logger import logger
from handlers import start_handler, menu_handler, message_handler, payment_handler, admin_handler

if __name__ == "__main__":
    logger.info("【 𝗟𝗢𝗦𝗜𝗘 】 Bot is starting...")
    init_db()
    logger.info("Database initialized. Bot going online!")
    try:
        bot.infinity_polling(none_stop=True, interval=0)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")