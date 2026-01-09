from telebot import types
from bot.instance import bot
from config.settings import NAGAD_NUMBER, ADMIN_USERNAME
from services.subscription_service import SubscriptionService
from datetime import datetime, timedelta

subscription_service = SubscriptionService()

def show_payment_options(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    stars_btn = types.KeyboardButton("⭐ Pay with Telegram Stars")
    nagad_30 = types.KeyboardButton("💸 Nagad - 100৳ (30 Days)")
    nagad_year = types.KeyboardButton("💸 Nagad - 400৳ (1 Year)")
    status_btn = types.KeyboardButton("🆓 Access Status")
    back_btn = types.KeyboardButton("🔙 Back to Menu")
    
    markup.add(stars_btn)
    markup.add(nagad_30, nagad_year)
    markup.add(status_btn, back_btn)
    
    text = """
🔒 আপনার প্রিমিয়াম অ্যাক্সেস শেষ হয়ে গেছে বা এখনো অ্যাকটিভ করা হয়নি।

💰 পেমেন্ট করে আনলক করুন:

⭐ <b>Telegram Stars (অটো আনলক)</b>
• ১টা ⭐ = ১ দিন ফুল প্রিমিয়াম

💸 <b>Nagad Manual</b>
• ১০০ টাকা = ৩০ দিন
• ৪০০ টাকা = ১ বছর (৩৬৫ দিন)

নিচ থেকে যেকোনো অপশন বেছে নিন 👇
    """.strip()
    
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

# Telegram Stars পেমেন্ট
def send_stars_invoice(chat_id):
    prices = [
        types.LabeledPrice("1 Day Premium", 1),     # 1 star
        types.LabeledPrice("7 Days Premium", 7),    # 7 stars
        types.LabeledPrice("30 Days Premium", 30),  # 30 stars
    ]
    
    bot.send_invoice(
        chat_id=chat_id,
        title="Losie Premium Access ⭐",
        description="প্রতি ১ Telegram Star = ১ দিন ফুল প্রিমিয়াম অ্যাক্সেস\nপেমেন্ট করলেই অটো আনলক হয়ে যাবে!",
        payload="premium_stars_access",
        provider_token="",  # Stars-এর জন্য খালি
        currency="XTR",
        prices=prices,
        start_parameter="stars-premium",
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False
    )

# Nagad ইনফো পাঠানো
def send_nagad_payment_info(chat_id, amount, days):
    text = f"""
💸 <b>Nagad Manual Payment</b>

🤑 অ্যামাউন্ট: <b>{amount} টাকা</b>
📅 অ্যাক্সেস: <b>{days} দিন</b>

📱 নম্বর: <code>{NAGAD_NUMBER}</code>
টাইপ: Personal

পেমেন্ট করার পর যেকোনো একটা সেন্ড করুন:
• TrxID (ট্রানজেকশন আইডি)
• * (স্টার) চাপলে যে মেসেজ আসে তার স্ক্রিনশট বা টেক্সট

আমি চেক করে খুব তাড়াতাড়ি আপনার অ্যাক্সেস অ্যাকটিভ করে দেব 🔥

সাপোর্ট: {ADMIN_USERNAME}
    """.strip()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Back to Payment Options")
    
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

# অ্যাক্সেস স্ট্যাটাস
def show_access_status(chat_id):
    user_id = chat_id  # চ্যাট আইডি = ইউজার আইডি প্রাইভেট চ্যাটে
    expiry = subscription_service.get_expiry_date(user_id)
    
    if expiry and expiry > datetime.now():
        days_left = (expiry - datetime.now()).days + 1
        bot.send_message(chat_id, f"✅ আপনার প্রিমিয়াম অ্যাক্সেস অ্যাকটিভ আছে!\n📅 বাকি: <b>{days_left} দিন</b>", parse_mode="HTML")
    else:
        show_payment_options(chat_id)

# পুরোনো ফাংশন (যদি অন্য ফাইল থেকে কল হয়)
def show_premium_required(chat_id):
    show_payment_options(chat_id)
