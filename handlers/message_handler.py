# handlers/message_handler.py
from telebot import types
from bot.instance import bot
from database.repository import get_user, update_category, increment_messages
from services.subscription_service import SubscriptionService
from utils.json_manager import get_random_response
from config.settings import PREMIUM_CATEGORIES, BOT_NAME, ADMIN_USERNAME
from handlers.payment_handler import show_premium_required
from handlers.menu_handler import show_main_menu

subscription_service = SubscriptionService()

# Button text → category type mapping
category_map = {
    "🤖 AI Chat": "free",
    "💕 Romantic": "free",
    "😏 Light Flirt": "free",
    "🔥 Sexy Chat": "premium",
    "😈 Dirty Talk": "premium",
    "🌶️ Hot Video": "premium",
    "🎤 Hot Voice": "premium",
    "🔞 Premium Content": "premium",
    "💰 Payment": "payment",
    "ℹ️ Info": "info"
}

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""
    
    # Track every message
    increment_messages(user_id)
    
    # Handle button clicks
    if text in category_map:
        action = category_map[text]
        
        if action == "payment":
            show_premium_required(message.chat.id)
            return
        
        if action == "info":
            info_text = f"""
<b>{BOT_NAME}</b>

🔞 Strictly 17+ | Ultimate Hot Chat Experience
🆓 First 30 Days Full Premium Access Free
💰 Payment: Manual via Nagad
📩 Activation & Support: {ADMIN_USERNAME}

Get ready to feel the heat 🔥
            """
            bot.send_message(message.chat.id, info_text)
            return
        
        # Free or Premium category selected
        # No need to save specific category name anymore (since random file is chosen)
        # But we can save the type for future analytics if needed
        update_category(user_id, action)  # saves "free" or "premium"
        
        # Premium check
        if action == "premium" and not subscription_service.is_active(user_id):
            show_premium_required(message.chat.id)
            return
        
        # Get random response from random file in that type
        response = get_random_response(action)
        
    else:
        # Ongoing normal chat (no button pressed)
        user = get_user(user_id)
        current_type = user["current_category"] if user else None
        
        # If previously selected premium but subscription expired
        if current_type == "premium" and not subscription_service.is_active(user_id):
            show_premium_required(message.chat.id)
            return
        
        # Use previous type or default to free
        response_type = current_type if current_type in ["free", "premium"] else "free"
        response = get_random_response(response_type)
    
    # Send the response (text, video, or voice)
    try:
        if response["type"] == "text":
            bot.send_message(message.chat.id, response["content"])
        elif response["type"] == "video":
            bot.send_video(
                message.chat.id,
                response["content"],
                caption="Enjoy this exclusive hot video 🔥"
            )
        elif response["type"] == "voice":
            bot.send_voice(
                message.chat.id,
                response["content"],
                caption="Listen to my naughty voice 🎤💦"
            )
    except Exception as e:
        bot.send_message(message.chat.id, "Oops! Something went wrong while sending content. Try again 🔥")
        print(f"Error sending media: {e}")