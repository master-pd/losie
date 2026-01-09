from telebot import types
from bot.instance import bot
from services.user_service import UserService
from config.constants import WELCOME_MESSAGE
from config.settings import BOT_NAME

user_states = {}  # Global state for registration flow
user_service = UserService()

# মেইন মেনু কীবোর্ড (রেজিস্ট্রেশনের পর দেখাবে)
def get_main_menu_keyboard(is_admin=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    free_trial_btn = types.KeyboardButton("🆓 Free Trial")
    payment_btn = types.KeyboardButton("💳 Payment Options")
    admin_contact_btn = types.KeyboardButton("👨‍💻 Admin Contact")
    
    markup.add(free_trial_btn, payment_btn)
    markup.add(admin_contact_btn)
    
    # যদি ইউজার অ্যাডমিন হয় তাহলে অতিরিক্ত বাটন (অপশনাল)
    if is_admin:
        admin_panel_btn = types.KeyboardButton("⚙️ Admin Panel")
        markup.add(admin_panel_btn)
    
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "None"
    
    user_service.register_user(user_id, first_name, username)
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_btn = types.KeyboardButton("📱 Share Phone Number", request_contact=True)
    markup.add(contact_btn)
    
    welcome_text = WELCOME_MESSAGE.format(
        first_name=first_name,
        bot_name=BOT_NAME
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    user_states[user_id] = "waiting_phone"

# Phone number রিসিভ করার হ্যান্ডলার (এটা অবশ্যই যোগ করো, না থাকলে phone share কাজ করবে না!)
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        
        # এখানে phone number সেভ করো ডাটাবেসে (তোমার user_service-এ ফাংশন থাকলে)
        user_service.update_phone(user_id, phone_number)  # যদি এই ফাংশন না থাকে তাহলে বানাও
        
        # অ্যাডমিন চেক করো (তোমার ডাটাবেসে admin list থাকলে)
        is_admin = user_service.is_admin(user_id)  # অথবা যেভাবে চেক করো
        
        bot.send_message(
            user_id,
            "🎉 ধন্যবাদ! রেজিস্ট্রেশন সম্পূর্ণ হয়েছে।\nএখন নিচের অপশনগুলো ব্যবহার করুন:",
            reply_markup=get_main_menu_keyboard(is_admin=is_admin)
        )
        
        # স্টেট ক্লিয়ার করো
        if user_id in user_states:
            del user_states[user_id]

# অ্যাডমিন প্যানেলের জন্য আলাদা কমান্ড
@bot.message_handler(commands=['admin'])
def handle_admin(message):
    user_id = message.from_user.id
    if user_service.is_admin(user_id):  # অ্যাডমিন চেক
        # এখানে অ্যাডমিন প্যানেলের কীবোর্ড বা মেসেজ পাঠাও
        admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # অ্যাডমিন বাটনগুলো যোগ করো, যেমন:
        admin_markup.add("📊 Stats", "👥 Users")
        admin_markup.add("🔄 Broadcast", "⚙️ Settings")
        admin_markup.add("🔙 Back to Menu")
        
        bot.send_message(user_id, "⚙️ অ্যাডমিন প্যানেলে স্বাগতম!", reply_markup=admin_markup)
    else:
        bot.send_message(user_id, "❌ আপনার অ্যাডমিন অ্যাক্সেস নেই।")
