# my imports
from timemodel import TimeModel

# standard imports
import time
import copy
import pprint
import sys

# 3rd party imports & aliases
import plotly
import plotly.graph_objs as go
from pymongo import MongoClient

# setup access to plotly API
plotly.tools.set_credentials_file(username='timothyCSnyder', api_key='mZ5dCnoJSLQ8CSq297Hc')


def main():
    n = int(sys.argv[1])
    db = sys.argv[2]

    start = time.time()
    sim  = runSeries(n, .5, 1, 1.7, .1)
    end = time.time()
    print("Time to generate: " + str(end - start) + " seconds")

    if(len(sys.argv) == 4 && sys.argv[3] == '-f'):
        print('fast')
        writeSeriesFast(sim, db)
    else:
        writeSeries(sim, db)

    

def runSeries(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    # saves current simulation snapshot to list and steps simulation
    for i in range(0, numIterations):
        series.append(copy.deepcopy(model))
        model.step()

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
