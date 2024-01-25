#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''
from functools import wraps
import redis
import requests
from typing import Callable


def cache_with_expiry(method: Callable) -> Callable:
    '''Define a decorator that tracks and sets an expired web cache'''
    @wraps(method)
    def wrapper(*args):
        _redis = redis.Redis()
        _redis.incr("count:{}".format(args[0]))
        cached = _redis.get("{}".format(args[0]))
        if cached:
            return cached.decode("utf-8")
        response = method(args[0])
        _redis.set("{}".format(args[0]), response, 10)
        return response
    return wrapper


@cache_with_expiry
def get_page(url: str) -> str:
    '''Return the content of an HTTP request'''
    response = requests.get(url)
    return response.text
