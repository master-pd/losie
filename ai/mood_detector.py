# ai/mood_detector.py: ইউজার মেসেজ থেকে ক্যাটেগরি/মুড ডিটেক্ট

from config.settings import PREMIUM_CATEGORIES, FREE_CATEGORIES

def detect_mood(message):
    message = message.lower()
    
    # কীওয়ার্ডস দিয়ে ক্যাটেগরি ডিটেক্ট
    keywords = {
        'sexy': ['sexy', 'সেক্সি', 'হট'],
        'dirty': ['dirty', 'ডার্টি', 'ময়লা', 'অপমান'],
        'hot_video': ['hot video', 'হট ভিডিও', 'ভিডিও'],
        'hot_voice': ['hot voice', 'হট ভয়েস', 'ভয়েস'],
        'flirt_intense': ['flirt intense', 'ইনটেন্স ফ্লার্ট', 'ফ্লার্ট জোরে'],
        'porn_video': ['porn video', 'পর্ন ভিডিও', 'পর্ন'],
        'ai_chat': ['ai chat', 'এআই চ্যাট', 'চ্যাট'],
        'love': ['love', 'ভালোবাসা', 'লাভ'],
        'romantic': ['romantic', 'রোমান্টিক', 'রোম্যান্স'],
        'flirt_light': ['flirt light', 'হালকা ফ্লার্ট', 'ফ্লার্ট']
    }
    
    for cat, words in keywords.items():
        if any(word in message for word in words):
            return cat
    
    # ডিফল্ট
    return 'romantic'
