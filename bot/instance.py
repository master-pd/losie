# bot/instance.py
from telebot import TeleBot
from config.settings import BOT_TOKEN

bot = TeleBot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview=True)
