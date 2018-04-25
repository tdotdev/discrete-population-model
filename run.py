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

    sim  = runSeries(n, .5, 1, 1.7, .1)
    print("Time to generate: " + str(sim['time']) + " seconds")

    #plotIt(sim[0])
    start = time.time()
    writeSeries(sim['series'], db)
    end = time.time()

    print("Mongo write time: " + str(end - start) + " seconds")

def runSeries(numIterations, initPopulation, initCapacity, alpha, amplitude):

    model = TimeModel(initPopulation, initCapacity, alpha, amplitude)
    series = []

    start_time = time.time()

    # saves current simulation snapshot to list and steps simulation
    for i in range(0, numIterations):
        series.append(copy.deepcopy(model))
        model.step()

    end_time = time.time()


    return {"series":series, "time":end_time - start_time}

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
    client = MongoClient()
    db = client['db']
    collection = db[collection]

    for j in range(0, len(series)):
        current = series[j]
        it = {"_id":j, "pop":current.population, "cap":current.capacity, "alp":current.alpha, "amp":current.amplitude}
        collection.insert_one(it)


if __name__ == "__main__":
    main()
