# handlers/admin/stats_handler.py
from bot.instance import bot
from utils.decorators import admin_only
from database.repository import get_user

@bot.message_handler(commands=['stats'])
@admin_only
def handle_stats(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /stats <user_id>")
            return
        
        user_id = int(parts[1])
        user = get_user(user_id)
        if not user:
            bot.reply_to(message, "User not found.")
            return
        
        stats = f"""
<b>User Stats - {user["first_name"]}</b>

ID: <code>{user["user_id"]}</code>
Phone: {user["phone"] or "Not shared"}
Age: {user["age"] or "Not shared"}
Messages Sent: {user["total_messages"]}
Premium Until: {user["premium_until"] or "Trial/Expired"}
Current Category: {user["current_category"] or "None"}
        """
        bot.reply_to(message, stats)
        
    except:
        bot.reply_to(message, "Invalid user ID.")