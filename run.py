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
    n = int(sys.argv[1])
    db = sys.argv[2]


    start = time.time()
    if(len(sys.argv) == 4 and sys.argv[3] == '-f'):
        #initPopulation, initCapacity, alpha, amplitude       
        sim  = runSeriesFast(n, .5, 1, 2.8, .1)
        end = time.time()
        writeSeriesFast(sim, db)
    else:
        #initPopulation, initCapacity, alpha, amplitude   
        sim  = runSeries(n, .5, 1, 1.7, .1)
        end = time.time()
        writeSeries(sim, db)


    print("Time to generate: " + str(end - start) + " seconds")
    

def runSeries(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    # saves current simulation snapshot to list and steps simulation
    for i in range(0, numIterations):
        series.append(copy.deepcopy(model))
        model.step()

    return series

def runSeriesFast(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    # saves current simulation snapshot to list and steps simulation
    for i in range(0, int(numIterations / 1000)):
        document = {'_id': i, 'val': []}
        for j in range(0, 1000):
            val = {'pop':model.population, 'cap':model.capacity, 'amp':model.amplitude, 'alp':model.alpha}
            document['val'].append(val)
            model.step()
        series.append(document)

    return series

def plotIt(series):
    x_data = []
    y_data = []

    n = len(series)
    i = 0

    while(i != n):
        x_data.append(series[i].t)
        y_data.append(series[i].population)
        i = i + 1


    trace = go.Scatter(
        x = x_data,
        y = y_data
    )

    data = [trace]
    plotly.plotly.iplot(data, filename='1000')

def writeSeries(series, collection):
    start = time.time()
    client = MongoClient()
    db = client['db']
    collection = db[collection]
    i = 0;

    for step in series:
        collection.insert_one({"_id":i, "pop":step.population, "cap":step.capacity, "alp":step.alpha, "amp":step.amplitude})
        i+=1
        


    end = time.time()
    print("Mongo write time: " + str(end - start) + " seconds")

def writeSeriesFast(series, collection):
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
