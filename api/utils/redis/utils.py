from redis import Redis
from decouple import config
from functools import lru_cache

@lru_cache()
def get_redis_connection():
    return Redis.from_url(config('REDIS_CACHE_URL'), decode_responses=True)

def cache_value(key: str, value:str, ex:str=None):
    redis_obj = get_redis_connection()
    redis_obj.set(key, value, ex)

def retrieve_value(key:str):
    redis_obj = get_redis_connection()
    return redis_obj.get(key)

def delete_value(key:str):
    redis_obj = get_redis_connection()
    redis_obj.delete(key)

