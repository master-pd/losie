# handlers/admin_handler.py - Full Advanced Admin Panel
from telebot import types
from bot.instance import bot
from utils.decorators import admin_only
from services.subscription_service import SubscriptionService
from database.repository import get_user, get_all_users
from config.settings import BOT_NAME, ADMIN_USERNAME
from datetime import datetime
import time

subscription_service = SubscriptionService()

@bot.message_handler(commands=['panel'])
@admin_only
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👥 Total Users", callback_data="admin_users"),
        types.InlineKeyboardButton("🔥 Active Premium", callback_data="admin_active")
    )
    markup.add(
        types.InlineKeyboardButton("🆕 New Today", callback_data="admin_today"),
        types.InlineKeyboardButton("📊 Full Stats", callback_data="admin_stats")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Broadcast (Soon)", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("⚙️ Settings (Soon)", callback_data="admin_settings")
    )
    
    panel_text = f"""
<b>{BOT_NAME} – Admin Panel ⚙️</b>

Welcome back, Admin!

<b>Available Commands:</b>
• /activate <user_id> <days> → Give free premium
• /stats <user_id> → View user details
• /panel → This dashboard

Quick stats below 👇

<i>স্বাগতম অ্যাডমিন! দ্রুত স্ট্যাটস দেখো নিচের বাটন থেকে</i>
    """.strip()
    
    bot.send_message(message.chat.id, panel_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_"))
def admin_callbacks(call):
    try:
        if call.data == "admin_users":
            total = len(get_all_users())
            bot.answer_callback_query(call.id, f"👥 Total Users: {total}", show_alert=True)
        
        elif call.data == "admin_active":
            active = subscription_service.count_active_premium()
            bot.answer_callback_query(call.id, f"🔥 Active Premium Users: {active}", show_alert=True)
        
        elif call.data == "admin_today":
            today = len(subscription_service.get_today_users())
            bot.answer_callback_query(call.id, f"🆕 New Users Today: {today}", show_alert=True)
        
        elif call.data == "admin_stats":
            total = len(get_all_users())
            active = subscription_service.count_active_premium()
            today = len(subscription_service.get_today_users())
            stats_text = f"""
<b>📊 Bot Statistics</b>

👥 Total Users: <b>{total}</b>
🔥 Active Premium: <b>{active}</b>
🆕 New Today: <b>{today}</b>

<i>Keep growing the heat 🔥</i>
            """.strip()
            bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id, parse_mode="HTML")
        
        elif call.data == "admin_broadcast":
            bot.answer_callback_query(call.id, "📢 Broadcast feature coming soon!", show_alert=True)
        
        elif call.data == "admin_settings":
            bot.answer_callback_query(call.id, "⚙️ Advanced settings coming soon!", show_alert=True)
            
    except Exception as e:
        bot.answer_callback_query(call.id, "Error loading data", show_alert=True)

@bot.message_handler(commands=['activate'])
@admin_only
def activate_user(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, 
                "❌ Usage: /activate <user_id> <days>\n"
                "Example: /activate 123456789 30\n\n"
                "<i>উদাহরণ: /activate 123456789 30</i>", 
                parse_mode="HTML")
            return
        
        user_id = int(parts[1])
        days = int(parts[2])
        
        if days <= 0:
            bot.reply_to(message, "❌ Days must be a positive number!")
            return
        
        subscription_service.extend_premium(user_id, days)
        expiry = subscription_service.get_expiry_date(user_id)
        expiry_str = expiry.strftime("%d %B %Y") if expiry else "Unknown"
        
        admin_reply = f"""
✅ <b>Free Premium Activated!</b>

👤 User ID: <code>{user_id}</code>
📅 Duration: <b>{days} days</b>
⏳ Expires: <b>{expiry_str}</b>

<i>সফলভাবে ফ্রি প্রিমিয়াম দেওয়া হয়েছে!</i>
        """.strip()
        
        bot.reply_to(message, admin_reply, parse_mode="HTML")
        
        # Notify the user
        try:
            user_notification = f"""
🎁 <b>Special Gift!</b>

🔥 Your premium has been activated <b>FREE</b> for <b>{days} days</b>!

😈 Unlimited hot videos, dirty talk, sexy voice – everything unlocked 💦

Enjoy baby... I'm all yours 🩷

<i>অ্যাডমিন তোমাকে {days} দিনের ফ্রি প্রিমিয়াম দিয়েছে!</i>
            """.strip()
            
            bot.send_message(user_id, user_notification, parse_mode="HTML")
        except:
            bot.reply_to(message, "⚠️ Activated, but user blocked the bot – couldn't notify.")
            
    except ValueError:
        bot.reply_to(message, "❌ Invalid format. User ID and days must be numbers.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['stats'])
@admin_only
def user_stats(message):
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
        
        is_active = subscription_service.is_active(user_id)
        premium_status = "Active 🔥" if is_active else "Expired"
        expiry = subscription_service.get_expiry_date(user_id)
        expiry_str = expiry.strftime("%d %B %Y") if expiry else "N/A"
        
        stats_text = f"""
<b>User Details & Stats</b>

👤 Name: {user["first_name"]}
🆔 ID: <code>{user["user_id"]}</code>
🎂 Age: {user["age"] or "Not provided"}
📅 Registered: {user["registration_date"][:10] if user["registration_date"] else "Unknown"}
💬 Total Messages: {user["total_messages"]}
🎯 Current Mode: {user["current_category"] or "Default"}
🔥 Premium Status: <b>{premium_status}</b>
⏳ Expires on: <b>{expiry_str}</b>

<i>ইউজারের সম্পূর্ণ তথ্য</i>
        """.strip()
        
        bot.reply_to(message, stats_text, parse_mode="HTML")
        
    except ValueError:
        bot.reply_to(message, "❌ Invalid user ID format.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")
