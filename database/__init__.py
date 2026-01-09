# database/__init__.py
from .repository import init_db, get_user, save_user, is_premium_active, activate_trial, update_category, increment_messages

__all__ = [
    "init_db", "get_user", "save_user", "is_premium_active",
    "activate_trial", "update_category", "increment_messages"
]