# config/master.py
"""
মাস্টার কনফিগারেশন ফাইল
নতুন ফিচার/জেনারেটর/রেসপন্স ফাইল যোগ করতে চাইলে শুধু নিচের লিস্টগুলোতে নাম যোগ করো
কোনো অন্য ফাইলে কোড পরিবর্তন করার দরকার নেই
"""

# -------------------------------------------------------------------------
# ১. AI জেনারেটর মডিউলের লিস্ট
# ফাইল নাম: ai/<module_name>_generator.py
# উদাহরণ: "girl_reply" → ai/girl_reply_generator.py
# -------------------------------------------------------------------------
ACTIVE_AI_GENERATORS = [
    "generator",           # GirlReplyGenerator (আনলিমিটেড টেক্সট রিপ্লাই)
    # নতুন জেনারেটর যোগ করতে চাইলে এখানে লাইন যোগ করো
    # "ultra_dirty",
    # "romantic_whisper",
    # "extreme_begging",
]

# -------------------------------------------------------------------------
# ২. JSON রেসপন্স ফাইলের লিস্ট (পুরোনো সিস্টেমের জন্য)
# পাথ: data/<filename>.json
# -------------------------------------------------------------------------
ACTIVE_RESPONSE_FILES = [
    #"data/ai.json",
    #"data/chat.json",
    #"data/dirty.json",
    #"data/flirt_intense.json",
    #"data/flirt_light.json",
    #"data/hot.json",
    #"data/hot_video.json",
    #"data/hot_voice.json",
    #"data/love.json",
    #"data/reply.json",
    #"data/responses_master.json",
    #"data/romantic.json",
    #"data/sexy.json",
    # নতুন JSON ফাইল যোগ করতে চাইলে এখানে যোগ করো
    # "data/new_extreme.json",
]

# -------------------------------------------------------------------------
# ৩. প্লাগইন মডিউলের লিস্ট (অন্যান্য ফিচারের জন্য)
# ফাইল নাম: plugins/<module_name>.py
# -------------------------------------------------------------------------
ACTIVE_PLUGINS = [
    #"photo_edit",           # ছবি এডিট ফিচার
    #"voice_generator",      # ভয়েস জেনারেটর
    # নতুন প্লাগইন যোগ করতে চাইলে এখানে যোগ করো
    # "sticker_maker",
]

# -------------------------------------------------------------------------
# হেল্পার ফাংশনসমূহ (অন্য ফাইল থেকে ইম্পোর্ট করে ব্যবহার করতে পারো)
# -------------------------------------------------------------------------

def get_ai_generator_modules():
    """সব অ্যাকটিভ AI জেনারেটরের মডিউল নাম রিটার্ন করে"""
    return [f"ai.{name}_generator" for name in ACTIVE_AI_GENERATORS]


def get_response_file_paths():
    """সব অ্যাকটিভ JSON রেসপন্স ফাইলের পুরো পাথ রিটার্ন করে"""
    return ACTIVE_RESPONSE_FILES


def get_plugin_modules():
    """সব অ্যাকটিভ প্লাগইনের মডিউল নাম রিটার্ন করে"""
    return [f"plugins.{name}" for name in ACTIVE_PLUGINS]


def print_active_status():
    """ডেভেলপমেন্টের জন্য — চালু অবস্থা প্রিন্ট করে"""
    print("===== Active Master Configuration =====")
    print(f"AI Generators ({len(ACTIVE_AI_GENERATORS)}):")
    for g in ACTIVE_AI_GENERATORS:
        print(f"  - {g}")
    print(f"\nResponse JSON Files ({len(ACTIVE_RESPONSE_FILES)}):")
    for f in ACTIVE_RESPONSE_FILES:
        print(f"  - {f}")
    print(f"\nPlugins ({len(ACTIVE_PLUGINS)}):")
    for p in ACTIVE_PLUGINS:
        print(f"  - {p}")
    print("=======================================")
