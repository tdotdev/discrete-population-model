# my imports
from timemodel import TimeModel

# standard imports
import time
import copy
import pprint
import sys

# 3rd party imports & aliases
from pymongo import MongoClient

def main():

    initPopulation = .5
    initCapacity = 1
    growthRate = 2.8
    amplitude = .1

    collection = []
    numIterations = int(sys.argv[1])
    collectionName = sys.argv[2]

    start = time.time()

    if(len(sys.argv) == 4 and sys.argv[3] == '-f'):
        #initPopulation, initCapacity, alpha, amplitude       
        collection = runSeriesFast(numIterations, initPopulation, initCapacity, growthRate, amplitude)

    else:
        collection  = runSeries(numIterations, initPopulation, initCapacity, growthRate, amplitude)
    
    end = time.time()

    print("Time to generate: " + str(end - start) + " seconds")
    writeSeries(collection, collectionName)
    

def runSeries(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    # saves current simulation snapshot to list and steps simulation
    for i in range(0, numIterations):
        series.append({"_id":i, "pop":model.population, "cap":model.capacity, "alp":model.alpha, "amp":model.amplitude})
        model.step()

    return series

def runSeriesFast(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    for i in range(0, int(numIterations / 1000)):
        document = {'_id': i, 'val': []}
        for j in range(0, 1000):
            document['val'].append({'pop':model.population, 'cap':model.capacity, 'amp':model.amplitude, 'alp':model.alpha})
            model.step()

        series.append(document)

    return series

def writeSeries(series, collection):
    start = time.time()
    client = MongoClient()
    db = client['db']
    collection = db[collection]
    i = 0;

    for doc in series:
        collection.insert_one(doc)
        i+=1
    
        
    end = time.time()
    print("Mongo write time: " + str(end - start) + " seconds")


if __name__ == "__main__":
    main()
