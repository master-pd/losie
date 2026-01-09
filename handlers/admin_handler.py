from telebot import types
from bot.instance import bot
from utils.decorators import admin_only
from services.subscription_service import SubscriptionService
from database.repository import get_user, get_all_users, get_today_users
from config.settings import ADMIN_USERNAME, BOT_NAME
import datetime

subscription_service = SubscriptionService()

@bot.message_handler(commands=['panel'])
@admin_only
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Total Users", callback_data="admin_total_users")
    )
    markup.add(
        types.InlineKeyboardButton("🔥 Active Premium", callback_data="admin_active_premium"),
        types.InlineKeyboardButton("🆕 Today's New", callback_data="admin_today_new")
    )

    panel_text = f"""
<b>{BOT_NAME} - Admin Panel ⚙️</b>

স্বাগতম, <b>{ADMIN_USERNAME}</b> 🔥

<i>উপলব্ধ কমান্ড:</i>
• /activate <user_id> <days>
• /stats <user_id>
• /broadcast (রিপ্লাই করে মেসেজ)
• /users - টোটাল স্ট্যাটস

আরও ফিচার শিগগিরই আসছে!
    """.strip()

    bot.send_message(message.chat.id, panel_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
@admin_only
def admin_callback(call):
    data = call.data

    if data == "admin_stats":
        # ভবিষ্যতে আরও স্ট্যাটস যোগ করতে পারো
        bot.answer_callback_query(call.id, "📊 Bot Stats coming soon!")

    elif data == "admin_total_users":
        all_users = len(get_all_users())
        bot.answer_callback_query(call.id, f"👥 Total Users: {all_users}")

    elif data == "admin_active_premium":
        active = subscription_service.count_active_premium()
        bot.answer_callback_query(call.id, f"🔥 Active Premium: {active}")

    elif data == "admin_today_new":
        today = len(get_today_users())
        bot.answer_callback_query(call.id, f"🆕 Today New Users: {today}")

@bot.message_handler(commands=['activate'])
@admin_only
def handle_activate(message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            bot.reply_to(message, "❌ সঠিক ফরম্যাট: /activate <user_id> <days>\nউদাহরণ: /activate 123456789 30")
            return
        
        user_id = int(parts[1])
        days = int(parts[2])
        
        if days <= 0:
            bot.reply_to(message, "❌ দিন পজিটিভ হতে হবে!")
            return
        
        subscription_service.extend_premium(user_id, days)
        
        # নতুন expiry দেখাও
        expiry = subscription_service.get_expiry_date(user_id)
        expiry_str = expiry.strftime("%d %B %Y") if expiry else "Unknown"
        
        success_msg = f"""
✅ <b>প্রিমিয়াম অ্যাকটিভেটেড!</b>

👤 User ID: <code>{user_id}</code>
📅 দিন যোগ: <b>{days}</b>
⏳ নতুন এক্সপায়ারি: <b>{expiry_str}</b>
        """.strip()
        
        bot.reply_to(message, success_msg, parse_mode="HTML")
        
        # ইউজারকে নোটিফাই
        try:
            bot.send_message(
                user_id,
                f"🎉 <b>অভিনন্দন!</b>\n\n"
                f"তোমার প্রিমিয়াম অ্যাক্সেস <b>{days} দিনের</b> জন্য অ্যাকটিভ করা হয়েছে!\n"
                f"এখন পুরোপুরি উপভোগ করো {BOT_NAME}-এর সাথে 🔥💦",
                parse_mode="HTML"
            )
        except:
            bot.reply_to(message, f"⚠️ অ্যাকটিভ হয়েছে, কিন্তু ইউজারকে মেসেজ পাঠানো যায়নি (ব্লক করেছে হয়তো)")

    except ValueError:
        bot.reply_to(message, "❌ ইউজার আইডি আর দিন নাম্বার হতে হবে।")
    except Exception as e:
        bot.reply_to(message, f"❌ এরর: {str(e)}")

@bot.message_handler(commands=['stats'])
@admin_only
def handle_stats(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ ব্যবহার: /stats <user_id>")
            return
        
        user_id = int(parts[1])
        user = get_user(user_id)
        
        if not user:
            bot.reply_to(message, "❌ এই ইউজার ডাটাবেসে পাওয়া যায়নি।")
            return
        
        is_active = subscription_service.is_active(user_id)
        status = "🟢 Active" if is_active else "🔴 Expired"
        
        expiry = subscription_service.get_expiry_date(user_id)
        expiry_str = expiry.strftime("%d %B %Y") if expiry else "No Premium"
        days_left = (expiry - datetime.datetime.now()).days + 1 if expiry and is_active else 0
        
        stats_text = f"""
<b>{BOT_NAME} - User Details</b>

👤 <b>ID:</b> <code>{user["user_id"]}</code>
👨 <b>Name:</b> {user["first_name"]}
📛 <b>Username:</b> @{user["username"] if user["username"] != "None" else "None"}
📱 <b>Phone:</b> {user["phone"] or "Not shared"}
💬 <b>Total Messages:</b> {user["total_messages"]}
🔥 <b>Current Chat:</b> {user["current_category"] or "None"}
⭐ <b>Premium Status:</b> {status}
⏳ <b>Expiry:</b> {expiry_str}
📅 <b>Days Left:</b> {days_left if is_active else 0}
📅 <b>Registered:</b> {user["registration_date"][:10]}
        """.strip()
        
        bot.reply_to(message, stats_text, parse_mode="HTML")
        
    except ValueError:
        bot.reply_to(message, "❌ ইউজার আইডি সঠিক নাম্বার হতে হবে।")

@bot.message_handler(commands=['users'])
@admin_only
def handle_users(message):
    total = len(get_all_users())
    today_new = len(get_today_users())
    active_premium = subscription_service.count_active_premium()
    
    text = f"""
📊 <b>{BOT_NAME} - Bot Statistics</b>

👥 মোট ইউজার: <b>{total}</b>
🆕 আজকের নতুন: <b>{today_new}</b>
🔥 অ্যাকটিভ প্রিমিয়াম: <b>{active_premium}</b>
    """.strip()
    
    bot.reply_to(message, text, parse_mode="HTML")

@bot.message_handler(commands=['broadcast'])
@admin_only
def handle_broadcast(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ ব্রডকাস্ট করতে যে মেসেজ পাঠাতে চাও, তার উপর রিপ্লাই করে /broadcast দাও।")
        return
    
    # কনফার্মেশন
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ হ্যাঁ, পাঠাও", callback_data=f"broadcast_confirm"),
        types.InlineKeyboardButton("❌ না", callback_data="broadcast_cancel")
    )
    
    bot.reply_to(message, "⚠️ তুমি কি নিশ্চিত যে সব ইউজারকে এই মেসেজ পাঠাতে চাও?", reply_markup=markup)
    
    # মেসেজ আইডি সেভ করো (গ্লোবাল ভ্যারিয়েবল বা ডাটাবেসে – সিম্পলের জন্য গ্লোবাল)
    global pending_broadcast
    pending_broadcast = message.reply_to_message

@bot.callback_query_handler(func=lambda call: call.data in ["broadcast_confirm", "broadcast_cancel"])
@admin_only
def broadcast_callback(call):
    global pending_broadcast
    
    if call.data == "broadcast_cancel":
        bot.edit_message_text("❌ ব্রডকাস্ট বাতিল করা হয়েছে।", call.message.chat.id, call.message.message_id)
        return
    
    if not pending_broadcast:
        bot.edit_message_text("❌ কোনো মেসেজ পেন্ডিং নেই।", call.message.chat.id, call.message.message_id)
        return
    
    bot.edit_message_text("🔄 ব্রডকাস্ট শুরু হচ্ছে... ধৈর্য ধরো।", call.message.chat.id, call.message.message_id)
    
    users = get_all_users()
    success = 0
    failed = 0
    
    for user in users:
        try:
            bot.forward_message(user["user_id"], pending_broadcast.chat.id, pending_broadcast.message_id)
            success += 1
        except:
            failed += 1
    
    result_text = f"""
✅ <b>ব্রডকাস্ট সম্পন্ন!</b>

📤 পাঠানো: <b>{success}</b>
❌ ফেইল্ড: <b>{failed}</b>
👥 মোট ইউজার: <b>{len(users)}</b>
    """.strip()
    
    bot.send_message(call.message.chat.id, result_text, parse_mode="HTML")
    pending_broadcast = None
