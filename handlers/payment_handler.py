# handlers/payment_handler.py - Telegram Stars Payment System
from telebot import types
from bot.instance import bot
from services.subscription_service import SubscriptionService
from config.settings import BOT_NAME
from datetime import datetime, timedelta
import time

subscription_service = SubscriptionService()

def show_payment_menu(chat_id):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1.5)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("⭐ Pay with Telegram Stars")
    markup.add("🆓 Access Status", "🔙 Back to Menu")
    
    text = f"""
🔒 <b>Your Premium Access Has Expired</b>

⭐ <b>Pay with Telegram Stars</b>

💎 <b>Rates:</b>
   • 1 ⭐ = 1 Day Full Premium
   • 7 ⭐ = 7 Days
   • 30 ⭐ = 30 Days (Best value!)

⚡ <b>Instant Auto Unlock!</b>
🔒 100% Safe & Hassle-free

Click below to pay with Stars 👇

<i>টেলিগ্রাম স্টার দিয়ে পেমেন্ট করো – পেমেন্ট হলেই অটো আনলক!</i>
    """.strip()
    
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

def send_stars_invoice(chat_id):
    prices = [
        types.LabeledPrice("1 Day Premium", 1 * 100),      # Telegram uses smallest unit
        types.LabeledPrice("7 Days Premium", 7 * 100),
        types.LabeledPrice("30 Days Premium", 30 * 100),
        types.LabeledPrice("90 Days Premium", 90 * 100),
        types.LabeledPrice("180 Days Premium", 180 * 100),
    ]
    
    bot.send_invoice(
        chat_id=chat_id,
        title=f"🔥 {BOT_NAME} Premium – Unlimited Access",
        description="1 ⭐ = 1 Day Unlimited Hot Content\n"
                    "Videos, Voice Notes, Dirty Talk – Everything Unlocked 😈\n"
                    "Instant activation after payment!",
        payload="losie_premium_stars_v1",
        provider_token="",  # Empty for Telegram Stars (XTR)
        currency="XTR",    # Telegram Stars currency
        prices=prices,
        start_parameter="premium-stars",
        photo_url="https://t.me/losie_promo/1",  # তোমার প্রোমো ছবির লিঙ্ক দাও (অপশনাল)
        photo_size=512,
        photo_width=512,
        photo_height=512,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True
    )

def show_access_status(chat_id, user_id=None):
    if user_id is None:
        user_id = chat_id
    
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)
    
    expiry = subscription_service.get_expiry_date(user_id)
    
    if expiry and expiry > datetime.now():
        days_left = (expiry - datetime.now()).days + 1
        text = f"""
✅ <b>Premium Active!</b>

📅 <b>{days_left} days</b> remaining
🔥 Enjoy unlimited hot content freely 😏

<i>প্রিমিয়াম চালু আছে – আরও {days_left} দিন ফুল ফান!</i>
        """.strip()
    else:
        text = """
🔒 <b>No Active Premium</b>

Your access has expired or trial ended.

⭐ Pay with Telegram Stars to unlock again!

<i>কোনো প্রিমিয়াম নেই – স্টার দিয়ে আনলক করো!</i>
        """
        show_payment_menu(chat_id)
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Back to Menu")
    
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

# Pre-checkout handler (required for Stars)
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    # Always approve Stars payments
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Successful payment handler
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    stars_paid = message.successful_payment.total_amount // 100  # Convert from smallest unit
    
    if payload == "losie_premium_stars_v1":
        # Extend premium by stars_paid days
        subscription_service.extend_premium(user_id, stars_paid)
        
        bot.send_chat_action(user_id, 'typing')
        time.sleep(1.5)
        
        success_text = f"""
🎉 <b>Payment Successful!</b>

⭐ You paid <b>{stars_paid} Telegram Stars</b>
🔥 <b>{stars_paid} days</b> Premium Access Added!

Now everything is unlocked again 😈💦

Enjoy the heat...

<i>পেমেন্ট সাকসেসফুল! {stars_paid} দিনের প্রিমিয়াম যোগ হয়েছে 🔥</i>
        """.strip()
        
        bot.send_message(user_id, success_text, parse_mode="HTML", reply_markup=get_main_menu_keyboard())

# Button handler for payment menu
@bot.message_handler(func=lambda m: m.text in ["⭐ Pay with Telegram Stars", "⭐ Payment"])
def handle_pay_with_stars(message):
    send_stars_invoice(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "🆓 Access Status")
def handle_access_status(message):
    show_access_status(message.chat.id, message.from_user.id)

@bot.message_handler(func=lambda m: m.text == "🔙 Back to Menu")
def handle_back_to_menu(message):
    from handlers.menu_handler import show_main_menu
    show_main_menu(message.chat.id)
