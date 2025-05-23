from datetime import datetime

_cache = {}

def set_cache(key, value, timeout=300):
    _cache[key] = {
        "data": value,
        "timestamp": datetime.now().timestamp(),
        "timeout": timeout
    }

def get_cache(key):
    entry = _cache.get(key)
    if not entry:
        return None
    if datetime.now().timestamp() - entry["timestamp"] > entry["timeout"]:
        _cache.pop(key)
        return None
    return entry["data"]
