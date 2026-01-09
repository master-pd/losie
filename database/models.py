# database/models.py - Future ORM support (placeholder)
class UserModel:
    def __init__(self, row):
        self.user_id = row["user_id"]
        self.first_name = row["first_name"]
        self.phone = row["phone"]
        self.age = row["age"]
        self.premium_until = row["premium_until"]
        self.current_category = row["current_category"]
        self.total_messages = row["total_messages"]