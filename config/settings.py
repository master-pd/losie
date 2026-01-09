# config/settings.py
import os

# Bot Settings
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with real token
ADMIN_ID = 123456789
ADMIN_USERNAME = "@ai_mar_pd"
PAYMENT_NUMBER = "01847634486"
BOT_NAME = "【 𝗟𝗢𝗦𝗜𝗘 】 ⟵o_𝗢"

# Database
DATABASE_PATH = "losie_data.db"

# Logging
LOG_FILE = "logs/bot.log"
os.makedirs("logs", exist_ok=True)

# Categories
PREMIUM_CATEGORIES = ["sexy", "dirty", "hot_video", "hot_voice", "flirt_intense", "porn_video"]
FREE_CATEGORIES = ["ai_chat", "love", "romantic", "flirt_light"]

# Trial
TRIAL_DAYS = 30