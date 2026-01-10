# utils/ai_reply_manager.py
"""
AI রিপ্লাই জেনারেট করার জন্য ম্যানেজার
config/master.py থেকে অ্যাকটিভ জেনারেটর লোড করে
"""

from config.master import ACTIVE_AI_GENERATORS
import importlib
from typing import Optional

# ক্যাশ (একবার লোড করা জেনারেটর রাখার জন্য)
_generator_instances = {}

def get_random_ai_reply(preferred: Optional[str] = None) -> str:
    """
    র্যান্ডম AI রিপ্লাই রিটার্ন করে
    preferred নাম দিলে সেইটা প্রায়োরিটি পাবে
    """
    global _generator_instances

    active = ACTIVE_AI_GENERATORS
    if not active:
        return "কোনো AI জেনারেটর চালু নেই। master.py চেক করো।"

    # প্রায়োরিটি চেক
    gen_name = preferred if preferred in active else active[0]

    if gen_name not in _generator_instances:
        try:
            # মডিউল লোড (যেমন: ai.generator → ai.generator.py)
            module = importlib.import_module(f"ai.{gen_name}")
            
            # ক্লাস নাম ফিক্সড: GirlReplyGenerator
            gen_class = getattr(module, "GirlReplyGenerator")
            _generator_instances[gen_name] = gen_class()
            
            print(f"AI generator loaded successfully: {gen_name}")
        except ImportError:
            return f"মডিউল পাওয়া যায়নি: ai.{gen_name}"
        except AttributeError:
            return f"ক্লাস GirlReplyGenerator পাওয়া যায়নি: ai.{gen_name}"
        except Exception as e:
            return f"জেনারেটর লোড ফেল: {str(e)}"

    try:
        return _generator_instances[gen_name].generate()
    except Exception as e:
        return f"রিপ্লাই জেনারেট করতে সমস্যা: {str(e)}"
