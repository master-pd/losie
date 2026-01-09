# handlers/start_handler.py
from telebot import types
from bot.instance import bot
from services.user_service import UserService
from config.constants import WELCOME_MESSAGE
from config.settings import BOT_NAME

user_states = {}  # Global state for registration flow
user_service = UserService()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "None"
    
    user_service.register_user(user_id, first_name, username)
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_btn = types.KeyboardButton("📱 Share Phone Number", request_contact=True)
    markup.add(contact_btn)
    
    welcome_text = WELCOME_MESSAGE.format(
        first_name=first_name,
        bot_name=BOT_NAME
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    user_states[user_id] = "waiting_phone"