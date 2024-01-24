#!/usr/bin/env python3
'''Cache class'''
import redis
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn: Optional[Callable]
            ) -> Union[None, str, bytes, int, float]:
        '''Return the key value converted to desired format'''
        return fn(self._redis.get(key)) if fn else self._redis.get(key)

    def get_str(self, key: str) -> Union[str, None]:
        '''Return the key value converted to string format'''
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        '''Return the key value converted to integer format'''
        return self.get(key, int)


# cache = Cache()

# TEST_CASES = {
#     b"foo": None,
#     123: int,
#     "bar": lambda d: d.decode("utf-8")
# }

# for value, fn in TEST_CASES.items():
#     key = cache.store(value)
#     assert cache.get(key, fn=fn) == value
