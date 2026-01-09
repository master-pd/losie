# utils/json_manager.py - Updated for master list of files
import json
import os
import random
from utils.logger import logger

DATA_FOLDER = "data"
MASTER_FILE = os.path.join(DATA_FOLDER, "responses_master.json")
_cache_master = None
_file_cache = {}

def load_master_list(force_reload=False):
    global _cache_master
    if _cache_master is None or force_reload:
        if not os.path.exists(MASTER_FILE):
            logger.error("responses_master.json not found!")
            return {"free": [], "premium": []}
        try:
            with open(MASTER_FILE, 'r', encoding='utf-8') as f:
                _cache_master = json.load(f)
            logger.info("Master file list loaded")
        except Exception as e:
            logger.error(f"Failed to load master list: {e}")
            _cache_master = {"free": [], "premium": []}
    return _cache_master

def load_single_json(filename):
    if filename in _file_cache:
        return _file_cache[filename]
    
    path = os.path.join(DATA_FOLDER, filename.strip())
    if not os.path.exists(path):
        logger.warning(f"JSON file not found: {filename}")
        return {"responses": [], "videos": [], "voices": []}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        _file_cache[filename] = data
        return data
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return {"responses": [], "videos": [], "voices": []}

def get_random_response(category_type: str):
    master = load_master_list()
    file_list = master.get(category_type, [])
    
    if not file_list:
        return {"type": "text", "content": "No content available yet... Coming soon 🔥"}
    
    chosen_file = random.choice(file_list)
    data = load_single_json(chosen_file)
    
    # Priority: responses > videos > voices
    if data.get("responses"):
        return {"type": "text", "content": random.choice(data["responses"])}
    
    if data.get("videos"):
        return {"type": "video", "content": random.choice(data["videos"])}
    
    if data.get("voices"):
        return {"type": "voice", "content": random.choice(data["voices"])}
    
    return {"type": "text", "content": f"Hot content from {chosen_file} loading... 🔥"}