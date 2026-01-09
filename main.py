# main.py - Bot entry point
from bot.instance import bot
from database.repository import init_db
from utils.logger import logger
from handlers import start_handler, menu_handler, message_handler, payment_handler, admin_handler

if __name__ == "__main__":
    logger.info("【 𝗟𝗢𝗦𝗜𝗘 】 Bot is starting...")
    init_db()
    logger.info("Database initialized. Bot going online!")
    try:
        bot.infinity_polling(none_stop=True, interval=0)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

from handlers.payment_handler import send_stars_invoice, send_nagad_payment_info, show_access_status

@bot.message_handler(func=lambda m: m.text == "⭐ Pay with Telegram Stars")
def handle_stars_payment(message):
    send_stars_invoice(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "💸 Nagad - 100৳ (30 Days)")
def handle_nagad_30(message):
    send_nagad_payment_info(message.chat.id, 100, 30)

@bot.message_handler(func=lambda m: m.text == "💸 Nagad - 400৳ (1 Year)")
def handle_nagad_year(message):
    send_nagad_payment_info(message.chat.id, 400, 365)

@bot.message_handler(func=lambda m: m.text == "🆓 Access Status")
def handle_status(message):
    show_access_status(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "🔙 Back to Payment Options")
def back_to_payment(message):
    from handlers.payment_handler import show_payment_options
    show_payment_options(message.chat.id)

# Telegram Stars সাকসেসফুল পেমেন্ট
@bot.successful_payment_handler()
def successful_stars_payment(message):
    user_id = message.chat.id
    stars = message.successful_payment.total_amount  # 1 star = 1 unit
    days_to_add = stars
    
    subscription_service.add_access_days(user_id, days_to_add)
    
    bot.send_message(user_id, f"🎉 ধন্যবাদ! পেমেন্ট সফল হয়েছে!\n⭐ {stars} Stars = {days_to_add} দিন প্রিমিয়াম আনলক হয়েছে 🔥\nএখন উপভোগ করুন!")

@bot.pre_checkout_query_handler(func=lambda q: True)
def pre_checkout_stars(query):
    bot.answer_pre_checkout_query(query.id, ok=True)
