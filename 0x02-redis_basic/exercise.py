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


def replay(method: Callable) -> None:
    '''Display the history of calls for a specific method'''
    key = method.__qualname__
    inputs = "{}:inputs".format(key)
    outputs = "{}:outputs".format(key)

    inputs = cache._redis.lrange(inputs, 0, -1)
    outputs = cache._redis.lrange(outputs, 0, -1)

    print("{} was called {} times:".format(
        key, cache.get(key).decode('utf-8')))
    for args, output in zip(inputs, outputs):
        args_str = args.decode('utf-8')  # Decode bytes to string
        output_str = output.decode('utf-8')  # Decode bytes to string
        print("{}(*{}) -> {}".format(key, args_str, output_str))


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
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
# Cache.store was called 3 times:
# Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
# Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
# Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
