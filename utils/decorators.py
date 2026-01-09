# utils/decorators.py
from functools import wraps
from telebot.types import Message
from bot.instance import bot
from config.settings import ADMIN_ID
from utils.logger import logger

def admin_only(func):
    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "❌ This command is for admin only.")
            logger.warning(f"Unauthorized access attempt by {message.from_user.id}")
            return
        return func(message, *args, **kwargs)
    return wrapper

def log_handler(func):
    @wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        logger.info(f"User {message.from_user.id} ({message.from_user.first_name}) triggered {func.__name__}")
        return func(message, *args, **kwargs)
    return wrapper