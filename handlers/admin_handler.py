# handlers/admin_handler.py - Admin commands only
from telebot import types
from bot.instance import bot
from utils.decorators import admin_only
from services.subscription_service import SubscriptionService
from database.repository import get_user
from config.settings import ADMIN_USERNAME, BOT_NAME
import datetime

subscription_service = SubscriptionService()

@bot.message_handler(commands=['activate'])
@admin_only
def handle_activate(message):
    """
    Usage: /activate <user_id> <days>
    Example: /activate 123456789 30
    """
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "❌ Usage: /activate <user_id> <days>\nExample: /activate 123456789 7")
            return
        
        user_id = int(parts[1])
        days = int(parts[2])
        
        if days <= 0:
            bot.reply_to(message, "❌ Days must be positive!")
            return
        
        subscription_service.extend_premium(user_id, days)
        
        success_msg = f"✅ Premium activated!\n\nUser ID: <code>{user_id}</code>\nDuration: {days} days"
        bot.reply_to(message, success_msg)
        
        # Notify the user
        try:
            bot.send_message(
                user_id,
                f"🎉 <b>Congratulations!</b>\n\n"
                f"Your premium access has been activated for <b>{days} days</b>!\n"
                f"Now enjoy unlimited hot content with {BOT_NAME} 🔥💦",
                parse_mode="HTML"
            )
        except:
            bot.reply_to(message, f"⚠️ Activated, but could not notify user {user_id} (maybe blocked bot)")
            
    except ValueError:
        bot.reply_to(message, "❌ Invalid format. User ID and days must be numbers.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['stats'])
@admin_only
def handle_stats(message):
    """
    Usage: /stats <user_id>
    Get user details and stats
    """
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ Usage: /stats <user_id>")
            return
        
        user_id = int(parts[1])
        user = get_user(user_id)
        
        if not user:
            bot.reply_to(message, "❌ User not found in database.")
            return
        
        premium_status = "Active" if subscription_service.is_active(user_id) else "Expired/Trial Ended"
        if user["premium_until"]:
            try:
                end_date = datetime.datetime.fromisoformat(user["premium_until"]).strftime("%d %B %Y")
                premium_status += f" (until {end_date})"
            except:
                pass
        
        stats_text = f"""
<b>{BOT_NAME} - User Stats</b>

<b>ID:</b> <code>{user["user_id"]}</code>
<b>Name:</b> {user["first_name"]}
<b>Username:</b> @{user["username"] if user["username"] != "None" else "Not set"}
<b>Phone:</b> {user["phone"] or "Not shared"}
<b>Age:</b> {user["age"] or "Not shared"}
<b>Total Messages:</b> {user["total_messages"]}
<b>Current Type:</b> {user["current_category"] or "None"}
<b>Premium Status:</b> {premium_status}
<b>Registered:</b> {user["registration_date"][:10] if user["registration_date"] else "Unknown"}
        """
        
        bot.reply_to(message, stats_text, parse_mode="HTML")
        
    except ValueError:
        bot.reply_to(message, "❌ Invalid user ID.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['broadcast'])
@admin_only
def handle_broadcast(message):
    """
    Simple broadcast - reply to a message with /broadcast
    """
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Please reply to a message you want to broadcast.")
        return
    
    # You can add confirmation later
    bot.reply_to(message, "⚠️ Broadcast feature coming soon! (Safety first)")
    # In future: send to all users

@bot.message_handler(commands=['panel'])
@admin_only
def admin_panel(message):
    """
    Admin quick panel
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📊 Bot Stats (Soon)", callback_data="admin_stats"))
    markup.add(types.InlineKeyboardButton("👥 Total Users (Soon)", callback_data="admin_users"))
    
    panel_text = f"""
<b>{BOT_NAME} - Admin Panel</b>

Welcome back, Admin {ADMIN_USERNAME} 🔥

Available commands:
• /activate <user_id> <days>
• /stats <user_id>
• /broadcast (reply to message)

More features coming soon!
    """
    bot.send_message(message.chat.id, panel_text, reply_markup=markup)
