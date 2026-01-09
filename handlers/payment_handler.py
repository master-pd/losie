# handlers/payment_handler.py
from telebot import types
from bot.instance import bot
from config.settings import PAYMENT_NUMBER, ADMIN_USERNAME
from config.constants import PREMIUM_LOCKED_MESSAGE

def show_premium_required(chat_id):
    markup = types.InlineKeyboardMarkup()
    admin_btn = types.InlineKeyboardButton("📩 Contact Admin for Activation", url=f"https://t.me/{ADMIN_USERNAME[1:]}")
    markup.add(admin_btn)
    
    text = PREMIUM_LOCKED_MESSAGE.format(
        payment_number=PAYMENT_NUMBER,
        admin_username=ADMIN_USERNAME
    )
    
    bot.send_message(chat_id, text, reply_markup=markup)