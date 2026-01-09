# services/subscription_service.py
from database.repository import is_premium_active, activate_trial, save_user
from config.settings import TRIAL_DAYS
import datetime
from utils.logger import logger

class SubscriptionService:
    def start_trial(self, user_id):
        activate_trial(user_id)
        logger.info(f"30-day premium trial started for user {user_id}")

    def is_active(self, user_id):
        return is_premium_active(user_id)

    def extend_premium(self, user_id, days):
        user = get_user(user_id)
        if user and user["premium_until"]:
            current_end = datetime.datetime.fromisoformat(user["premium_until"])
        else:
            current_end = datetime.datetime.now()
        new_end = current_end + datetime.timedelta(days=days)
        save_user(user_id, {"premium_until": new_end.isoformat()})
        logger.info(f"Premium extended for user {user_id} by {days} days")