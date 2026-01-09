# database/repository.py
from database.connection import get_connection
from config.settings import TRIAL_DAYS
from utils.logger import logger
import datetime

def init_db():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        phone TEXT,
        age INTEGER,
        registration_date TEXT,
        premium_until TEXT,
        current_category TEXT,
        total_messages INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def get_user(user_id):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def save_user(user_id, updates: dict):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    user = get_user(user_id)
    
    data = {
        "first_name": updates.get("first_name", user["first_name"] if user else None),
        "username": updates.get("username", user["username"] if user else None),
        "phone": updates.get("phone", user["phone"] if user else None),
        "age": updates.get("age", user["age"] if user else None),
        "registration_date": updates.get("registration_date", user["registration_date"] if user else datetime.datetime.now().isoformat()),
        "premium_until": updates.get("premium_until", user["premium_until"] if user else None),
        "current_category": updates.get("current_category", user["current_category"] if user else None),
        "total_messages": updates.get("total_messages", user["total_messages"] if user else 0)
    }
    
    cursor.execute("""INSERT OR REPLACE INTO users 
        (user_id, first_name, username, phone, age, registration_date, premium_until, current_category, total_messages)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, data["first_name"], data["username"], data["phone"], data["age"],
         data["registration_date"], data["premium_until"], data["current_category"], data["total_messages"]))
    conn.commit()
    conn.close()

def is_premium_active(user_id):
    user = get_user(user_id)
    if not user or not user["premium_until"]:
        return False
    try:
        end_date = datetime.datetime.fromisoformat(user["premium_until"])
        return datetime.datetime.now() < end_date
    except:
        return False

def activate_trial(user_id):
    end_date = datetime.datetime.now() + datetime.timedelta(days=TRIAL_DAYS)
    save_user(user_id, {"premium_until": end_date.isoformat()})
    logger.info(f"Trial activated for user {user_id}")

def update_category(user_id, category):
    save_user(user_id, {"current_category": category})

def increment_messages(user_id):
    user = get_user(user_id)
    if user:
        new_count = user["total_messages"] + 1
        save_user(user_id, {"total_messages": new_count})

def get_today_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute("SELECT * FROM users WHERE registration_date LIKE ?", (f"{today}%",))
    users = cursor.fetchall()
    conn.close()
    return users

def count_active_premium():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE premium_until > DATETIME('now')")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_users():
    """সব ইউজারের লিস্ট রিটার্ন করে"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    # SQLite থেকে ডিকশনারি ফরম্যাটে কনভার্ট (যাতে admin_handler-এ কাজ করে)
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, user)) for user in users]

def get_today_users():
    """আজকের রেজিস্টার করা ইউজারের লিস্ট"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute("SELECT * FROM users WHERE DATE(registration_date) = ?", (today,))
    users = cursor.fetchall()
    conn.close()
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, user)) for user in users]

def count_active_premium():
    """অ্যাকটিভ প্রিমিয়াম ইউজারের সংখ্যা"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE expiry_date > DATETIME('now')")
    count = cursor.fetchone()[0]
    conn.close()
    return count
