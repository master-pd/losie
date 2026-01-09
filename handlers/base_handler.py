# handlers/base_handler.py
# Base class for common functionality
class BaseHandler:
    def __init__(self):
        from services.user_service import UserService
        from services.subscription_service import SubscriptionService
        self.user_service = UserService()
        self.subscription_service = SubscriptionService()