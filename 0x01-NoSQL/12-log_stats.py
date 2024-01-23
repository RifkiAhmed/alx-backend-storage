#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["logs"]
collection = db["nginx"]
print(f"{collection.count_documents({})} logs")
print("Methods:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    print("    method {}: {}".format(
        method,
        collection.count_documents({"method": method})
    ))

print("{} status check".format(
    collection.count_documents({'method': 'GET', 'path': '/status'})
))
