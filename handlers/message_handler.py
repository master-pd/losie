from telebot import types
from bot.instance import bot
from database.repository import get_user, update_category, increment_messages
from services.subscription_service import SubscriptionService
from utils.json_manager import get_random_response
from config.settings import PREMIUM_CATEGORIES, BOT_NAME, ADMIN_USERNAME, NAGAD_NUMBER
from handlers.payment_handler import show_payment_options  # আমরা নতুন পেমেন্ট হ্যান্ডলার বানাব
from handlers.menu_handler import show_main_menu
import datetime
from config.master import get_response_file_paths, get_ai_generator_modules
from utils.ai_reply_manager import get_random_ai_reply  

subscription_service = SubscriptionService()

# বাটন ম্যাপিং
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
    "ℹ️ Info": "info",
    "🆓 Trial Status": "status"
}

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""
    
    # প্রতিটি মেসেজ ট্র্যাক করো
    increment_messages(user_id)
    
    # বাটন ক্লিক হ্যান্ডল
    if text in category_map:
        action = category_map[text]
        
        if action == "payment":
            show_payment_options(message.chat.id)
            return
        
        if action == "info":
            info_text = f"""
<b>{BOT_NAME} 🔥</b>

🔞 Strictly 17+ | Ultimate Hot Chat Experience
🆓 প্রথম ৩০ দিন ফুল প্রিমিয়াম ফ্রি!
💰 পেমেন্ট: Nagad Manual বা Telegram Stars ⭐
⭐ ১টা Star = ১ দিন অ্যাক্সেস (অটো আনলক)
💸 Nagad: ১০০৳ = ৩০ দিন | ৪০০৳ = ১ বছর
📩 সাপোর্ট & অ্যাকটিভেশন: {ADMIN_USERNAME}

Get ready to feel the heat 🔥😈
            """.strip()
            bot.send_message(message.chat.id, info_text, parse_mode="HTML")
            return
        
        if action == "status":
            expiry = subscription_service.get_expiry_date(user_id)
            if expiry:
                days_left = (expiry - datetime.datetime.now()).days + 1
                bot.send_message(message.chat.id, f"🆓 আপনার প্রিমিয়াম অ্যাক্সেস বাকি: <b>{days_left} দিন</b>", parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, "🔒 কোনো অ্যাক্টিভ প্রিমিয়াম নেই। পেমেন্ট করুন 💰")
            return
        
        # ক্যাটাগরি সিলেক্ট করা হয়েছে
        update_category(user_id, action)
        
        # প্রিমিয়াম চেক
        if action in PREMIUM_CATEGORIES and not subscription_service.is_active(user_id):
            show_payment_options(message.chat.id)
            return
    
    # নরমাল চ্যাট বা ক্যাটাগরি সিলেক্টের পর চ্যাট চলবে
    user = get_user(user_id)
    current_type = user["current_category"] if user else "free"
    
    if current_type in PREMIUM_CATEGORIES and not subscription_service.is_active(user_id):
        show_payment_options(message.chat.id)
        return
    
    # AI generator থেকে রিপ্লাই নেওয়া
    try:
        content = get_random_ai_reply()  # এটাই তোমার আনলিমিটেড র্যান্ডম রিপ্লাই দিবে
        
        # সবসময় টেক্সট হিসেবে পাঠানো (কারণ generator শুধু টেক্সট দেয়)
        bot.send_message(message.chat.id, content)
    
    except Exception as e:
        bot.send_message(message.chat.id, "উফ! কিছু একটা গন্ডগোল হয়েছে। আবার ট্রাই করো 🔥")
        print(f"AI Reply Error: {e}")
