# services/user_service.py
from database.repository import get_user, save_user, increment_messages
from utils.logger import logger

class UserService:
    def register_user(self, user_id, first_name, username=None):
        save_user(user_id, {
            "first_name": first_name,
            "username": username,
            "registration_date": datetime.datetime.now().isoformat()
        })
        logger.info(f"New user registered: {user_id} ({first_name})")

    def update_phone(self, user_id, phone):
        save_user(user_id, {"phone": phone})

    def update_age(self, user_id, age):
        save_user(user_id, {"age": age})

    def track_message(self, user_id):
        increment_messages(user_id)