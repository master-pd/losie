# handlers/registration/age_handler.py
from telebot import types
from bot.instance import bot
from services.user_service import UserService
from services.subscription_service import SubscriptionService
from config.constants import TRIAL_SUCCESS_MESSAGE
from config.settings import BOT_NAME, TRIAL_DAYS
from handlers.menu_handler import show_main_menu

user_states = {}  # Shared with other registration handlers
user_service = UserService()
subscription_service = SubscriptionService()

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_age")
def handle_age(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    try:
        age = int(message.text.strip())
        if age < 17:
            bot.send_message(message.chat.id, "❌ Sorry, this bot is strictly for 17+ users only.")
            del user_states[user_id]
            return
        
        user_service.update_age(user_id, age)
        subscription_service.start_trial(user_id)
        del user_states[user_id]
        
        success_msg = TRIAL_SUCCESS_MESSAGE.format(
            first_name=first_name,
            trial_days=TRIAL_DAYS
        )
        bot.send_message(message.chat.id, success_msg)
        show_main_menu(message.chat.id)
        
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Please enter your age using numbers only (e.g., 25).")