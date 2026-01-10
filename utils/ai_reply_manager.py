# utils/ai_reply_manager.py
from config.master import ACTIVE_AI_GENERATORS
import importlib

# ক্যাশ (একবার লোড করা জেনারেটর রাখার জন্য)
_generator_instances = {}

def get_random_ai_reply():
    if not ACTIVE_AI_GENERATORS:
        return "কোনো AI জেনারেটর চালু নেই 😔"
    
    # প্রথম অ্যাকটিভ জেনারেটর নাও (পরে চাইলে র্যান্ডম করতে পারো)
    gen_name = ACTIVE_AI_GENERATORS[0]
    
    if gen_name not in _generator_instances:
        try:
            module = importlib.import_module(f"ai.{gen_name}_generator")
            gen_class = getattr(module, "GeneratorClass")
            _generator_instances[gen_name] = gen_class()
        except Exception as e:
            return f"জেনারেটর লোড করতে সমস্যা: {str(e)}"
    
    return _generator_instances[gen_name].generate()
