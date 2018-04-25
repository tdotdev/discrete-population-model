# my imports
from timemodel import TimeModel

# standard imports
import time
import copy
import pprint

# 3rd party imports & aliases
import plotly
import plotly.graph_objs as go
from pymongo import MongoClient

# setup access to plotly API
plotly.tools.set_credentials_file(username='timothyCSnyder', api_key='mZ5dCnoJSLQ8CSq297Hc')


def main():
    # mongo declarations

    # simulation bounds
    n = 100;
    i = 0
    series = []

    model = TimeModel(.5, 1, 1.7, .1)

    print("Start population:\t" + str(model.population))

    start_time = time.time()

    # saves current simulation snapshot to list and steps simulation
    while(i != n):
        series.append(copy.deepcopy(model))

        model.step()
        i = i + 1;

    end_time = time.time()

    print("End population:\t\t" + str(model.population))
    print("Time:\t\t\t" + str(end_time - start_time) + "s")
    print("Total iterations:\t" + str(len(series)))

    plotIt(series)
    writeSeries(series, 'series2')


def runSeries(start, end):
    

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
    #plotly.plotly.iplot(data, filename='1000')

def writeSeries(series, collection):
    client = MongoClient()
    db = client.dts_database
    collection = db[collection]

    for j in range(0, len(series)):
        current = series[j]
        it = {"_id":j, "pop":current.population, "cap":current.capacity, "alp":current.alpha, "amp":current.amplitude}
        collection.insert_one(it)

    print(db.collection_names(include_system_collections=False))
    for i in collection.find():
        pprint.pprint(i)


if __name__ == "__main__":
    main()
