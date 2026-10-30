from redis import Redis
import json

redis = Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

def get_cache(key):

    data = redis.get(key)

    if data is None:
        return None

    return json.loads(data)

def set_cache(key, value):

    redis.set(key, json.dumps(value), ex=600)

def clear_cache(key):

    redis.delete(key)

def clear_cache_pattern(pattern):

    for key in redis.scan_iter(match=pattern):
        redis.delete(key)
