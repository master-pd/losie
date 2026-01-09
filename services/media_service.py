# services/media_service.py
# Placeholder for future media upload/download management
class MediaService:
    def send_content(self, chat_id, response):
        from bot.instance import bot
        if response["type"] == "text":
            bot.send_message(chat_id, response["content"])
        elif response["type"] == "video":
            bot.send_video(chat_id, response["content"])
        elif response["type"] == "voice":
            bot.send_voice(chat_id, response["content"])