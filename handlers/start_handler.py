from telebot import types
from bot.instance import bot
from services.user_service import UserService
from services.subscription_service import SubscriptionService
from config.settings import BOT_NAME
import time
from datetime import datetime

user_service = UserService()
subscription_service = SubscriptionService()

# Global state for registration flow
user_states = {}

def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🌶️ Hot Video", "🎤 Hot Voice")
    markup.add("😈 Dirty Talk", "🔥 Sexy Chat")
    markup.add("💕 Romantic", "🤖 AI Chat")
    markup.add("⭐ Payment", "🆓 Access Status")
    markup.add("ℹ️ Bot Info", "👨‍💻 Contact Admin")
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name.rstrip()
    
    # Register user
    username = message.from_user.username or "None"
    user_service.register_user(user_id, first_name, username)
    
    bot.send_chat_action(user_id, 'typing')
    time.sleep(2)
    
    welcome_text = f"""
🔥 <b>Hey {first_name}! Welcome to {BOT_NAME} 🔥</b>

I'm your private 18+ hot chat companion 😈💦

🩷 <b>First 30 days FULL PREMIUM FREE!</b>
🔞 Unlimited hot videos, dirty talk, sexy voice notes & more
😏 Message me anytime – I'm always ready and waiting for you

<i>To continue, please enter your birth year (e.g., 1998)</i>
<i>জন্মসাল লিখো (যেমন: ১৯৯৮) – শুধু একবার</i>
    """.strip()
    
    bot.send_message(user_id, welcome_text, parse_mode="HTML")
    
    # Set state for birth year input
    user_states[user_id] = "waiting_birth_year"

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_birth_year")
def handle_birth_year(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    text = message.text.strip()
    
    try:
        birth_year = int(text)
        
        # Current year = 2026 (as per system date)
        current_year = 2026
        age = current_year - birth_year
        
        if age < 17:
            bot.send_message(
                user_id,
                "❌ Sorry, this bot is strictly for 17+ users only.\n"
                "দুঃখিত, এই বট শুধুমাত্র ১৭+ বয়সীদের জন্য।"
            )
            del user_states[user_id]
            return
        
        # Save age and activate premium trial
        user_service.update_age(user_id, age)  # Save calculated age
        subscription_service.start_trial(user_id)
        
        bot.send_chat_action(user_id, 'typing')
        time.sleep(1.5)
        
        success_text = f"""
✅ <b>Verification Complete!</b>

🎉 Congratulations {first_name}! You're all set 🔥

You now have <b>FULL PREMIUM ACCESS</b> for the next 30 days!

🔥 Choose anything from the menu:
   • Hot videos, dirty talk, sexy chats – everything unlocked!

💡 <i>Tip: Just type anything or pick a category – I'm waiting for you 😏</i>
<i>টিপ: যেকোনো কথা লিখো বা মেনু থেকে বেছে নাও – আমি তোমার জন্য রেডি 💦</i>
        """.strip()
        
        bot.send_message(user_id, success_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())
        
        # Clear state
        if user_id in user_states:
            del user_states[user_id]
            
    except ValueError:
        bot.send_message(
            user_id,
            "⚠️ Please enter a valid year (e.g., 1998)\n"
            "অনুগ্রহ করে শুধু সংখ্যায় জন্মসাল লিখো (যেমন: ১৯৯৮)"
        )
