#!/usr/bin/env python3
'''Cache class'''
import redis
from typing import Union


class Cache:
    '''Define class Cache'''

    def __init__(self) -> None:
        '''Initiate instance and store an instance of the Redis client'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store the input data in Redis instance'''
        import uuid
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


# cache = Cache()

# data = b"hello"
# key = cache.store(data)
# print(key)

# local_redis = redis.Redis()
# print(local_redis.get(key))
