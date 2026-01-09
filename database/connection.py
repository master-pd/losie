# database/connection.py
import sqlite3
from config.settings import DATABASE_PATH
from utils.logger import logger

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None