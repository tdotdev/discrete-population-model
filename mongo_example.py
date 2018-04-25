from pymongo import MongoClient

client = MongoClient()
db = client.test_database
collection = db.test_collection

import datetime
post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}

db.posts.insert_one(post)

print(db.collection_names(include_system_collections=False))