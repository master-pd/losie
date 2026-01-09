# handlers/menu_handler.py
from telebot import types
from bot.instance import bot
from config.settings import BOT_NAME

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🤖 AI Chat", "💕 Romantic",
        "😏 Light Flirt", "🔥 Sexy Chat",
        "😈 Dirty Talk", "🌶️ Hot Video",
        "🎤 Hot Voice", "🔞 Premium Content",
        "💰 Payment", "ℹ️ Info"
    ]
    markup.add(*buttons[:2])
    markup.add(*buttons[2:4])
    markup.add(*buttons[4:6])
    markup.add(*buttons[6:8])
    markup.add(*buttons[8:10])
    
    bot.send_message(
        chat_id,
        f"<b>{BOT_NAME}</b>\n\nSelect your fantasy tonight 👅",
        reply_markup=markup
    )