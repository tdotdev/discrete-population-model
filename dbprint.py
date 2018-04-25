import sys
import pprint
from pymongo import MongoClient

client = MongoClient()

db = client.dts_database

collection = db[sys.argv[1]]

for documents in collection.find():
	pprint.pprint(documents)