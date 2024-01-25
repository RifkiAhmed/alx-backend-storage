#!/usr/bin/env python3
'''Cache class'''
from functools import wraps
import redis
from typing import Union, Optional, Callable
import uuid


def count_calls(method: Callable) -> Callable:
    '''Decorator to count how many times methods are called'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''''''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator to store the history of inputs and outputs for methods'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''''''
        key = method.__qualname__
        inputs = "{}:inputs".format(key)
        outputs = "{}:outputs".format(key)
        self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(output))
        return output
    return wrapper


class Cache:
    '''Define class Cache'''

    def __init__(self) -> None:
        '''Initiate instance and store an instance of the Redis client'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange(
    "{}:inputs".format(
        cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange(
    "{}:outputs".format(
        cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))
