import sys
import pprint
import time
from pymongo import MongoClient

client = MongoClient()

def main():
	cmd = sys.argv[1]
	arg1 = sys.argv[2]

	if(cmd == "dropdb"):
		dropdb(sys.argv[2])

	elif(cmd == "printdb"):
		printdb(sys.argv[2])

	elif(cmd == "readcol"):
		readcol(sys.argv)

	elif(cmd == "dropcol"):
		dropcol(sys.argv)

def dropdb(arg):
	print("Delete " + arg + "\nAre you sure? [y/n]")
	response = input()
	if(response == "y"):
		client.drop_database(arg)
		print(arg + " deleted.")

def printdb(arg):
	db = client[arg]
	print(db.collection_names(include_system_collections=False))

def dropcol(args):
	db = client[args[2]]
	collection = db[args[3]]
	collection.drop()
	print(args[3] + " deleted.")

def readcol(args):

	db = client[args[2]]
	collection = db[args[3]]
	printFlag = False

	start = time.time()

	for document in collection.find():
		x = str(document)
		if(len(args) == 5 and args[4] == "-p"):
			pprint.pprint(x)
			printFlag = True

	end = time.time()

	if(not printFlag):
		print("Read time: " + str(end - start) + " seconds")

if __name__ == "__main__":
    main()