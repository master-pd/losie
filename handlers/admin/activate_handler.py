# handlers/admin/activate_handler.py
from bot.instance import bot
from utils.decorators import admin_only
from services.subscription_service import SubscriptionService
import datetime

subscription_service = SubscriptionService()

@bot.message_handler(commands=['activate'])
@admin_only
def handle_activate(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Usage: /activate <user_id> <days>")
            return
        
        user_id = int(parts[1])
        days = int(parts[2])
        
        subscription_service.extend_premium(user_id, days)
        
        bot.reply_to(message, f"✅ Premium activated for user {user_id} for {days} days.")
        bot.send_message(user_id, "🎉 Your premium access is now active! Dive into the heat 🔥")
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")