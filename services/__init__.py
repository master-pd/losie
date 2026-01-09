# services/__init__.py
from .user_service import UserService
from .subscription_service import SubscriptionService

user_service = UserService()
subscription_service = SubscriptionService()