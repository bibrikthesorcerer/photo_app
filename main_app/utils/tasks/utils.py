import redis
from decouple import config

def cache_deletion_to_redis(obj_id, task_id):
    r = redis.from_url(config('REDIS_URL'))
    try:
        r.set("photoDel:" + str(obj_id), task_id)
    except redis.ConnectionError:
        print('Unable to reach Redis')

def remove_deletion_from_redis(obj_id):
    r = redis.from_url(config("REDIS_URL"))
    try:
        key = "photoDel:" + str(obj_id)
        task_id = r.get(key)
        print(r.delete(key))
        return task_id
    except redis.ConnectionError:
        print('Unable to reach Redis')
