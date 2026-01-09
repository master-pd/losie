# handlers/menu_handler.py - Advanced Main Menu
from telebot import types
from bot.instance import bot
from config.settings import BOT_NAME
import time

def get_main_menu_keyboard():
    """
    Returns the main menu keyboard
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Row 1
    markup.add("🌶️ Hot Video", "🎤 Hot Voice")
    # Row 2
    markup.add("😈 Dirty Talk", "🔥 Sexy Chat")
    # Row 3
    markup.add("💕 Romantic", "🤖 AI Chat")
    # Row 4
    markup.add("😏 Light Flirt", "🔞 Premium Content")
    # Row 5
    markup.add("💰 Payment", "🆓 Access Status")
    # Row 6
    markup.add("ℹ️ Bot Info", "👨‍💻 Contact Admin")
    
    return markup

def show_main_menu(chat_id):
    """
    Shows the main menu with animation and hot message
    """
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1.2)
    
    menu_text = f"""
<b>{BOT_NAME}</b>

🔥 <b>What turns you on tonight?</b> 😈

Choose your fantasy from the menu below 👅

<i>আজ রাতে কী চাও? মেনু থেকে বেছে নাও 😏</i>
    """.strip()
    
    bot.send_message(
        chat_id,
        menu_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )
