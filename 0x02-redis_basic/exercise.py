#!/usr/bin/env python3
'''Cache class'''
from functools import wraps
import redis
from typing import Union, Optional, Callable
import uuid


def count_calls(method: Callable) -> Callable:
    '''Count how many times methods are called'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''''''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    '''Define class Cache'''

    def __init__(self) -> None:
        '''Initiate instance and store an instance of the Redis client'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store the input data in Redis instance'''
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[None, str, bytes, int, float]:
        '''Return the key value converted to desired format'''
        value = self._redis.get(key)
        return fn(value) if fn and value else self._redis.get(key)

    def get_str(self, key: str) -> Union[str, None]:
        '''Return the key value converted to string format'''
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        '''Return the key value converted to integer format'''
        return self.get(key, int)


# cache = Cache()

# cache.store(b"first")
# print(cache.get(cache.store.__qualname__))

# cache.store(b"second")
# cache.store(b"third")
# print(cache.get(cache.store.__qualname__))
