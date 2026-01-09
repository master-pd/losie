# handlers/registration/phone_handler.py
from telebot import types
from bot.instance import bot
from services.user_service import UserService

user_states = {}
user_service = UserService()

@bot.message_handler(content_types=['contact'])
def handle_phone(message):
    user_id = message.from_user.id
    if user_states.get(user_id) != "waiting_phone":
        return
    
    phone = message.contact.phone_number
    user_service.update_phone(user_id, phone)
    
    bot.send_message(message.chat.id, "Phone saved ✅\n\nNow enter your age (numbers only):")
    user_states[user_id] = "waiting_age"