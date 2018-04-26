import sys

# 3rd party imports & aliases
import plotly
import plotly.graph_objs as go
from pymongo import MongoClient

# setup access to plotly API
plotly.tools.set_credentials_file(username='timothyCSnyder', api_key='mZ5dCnoJSLQ8CSq297Hc')


def main():

	client = MongoClient()
	db = client['db']
	collection = db[sys.argv[1]]

	populationSize = []
	timeN = []


	for document in collection.find():
		doc = document
		val = doc['val']
		for i in range (0, 100):
			if(val[i]['pop'] > 0):
				populationSize.append(val[i]['pop'])
				timeN.append(i)


	trace = go.Scatter(x = timeN,y = populationSize)

	data = [trace]
	plotly.plotly.iplot(data, filename=sys.argv[1])

if __name__ == "__main__":
    main()