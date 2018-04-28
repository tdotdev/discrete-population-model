import sys

# 3rd party imports & aliases
import plotly
import plotly.graph_objs as go
from pymongo import MongoClient

# setup access to plotly API
plotly.tools.set_credentials_file(username='user', api_key='key')


def main():

	client = MongoClient()
	db = client['db']
	collection = db[sys.argv[1]]

	populationSize = []
	zeroToN = []

	for document in collection.find():
		for i in range (0, 100):
			rec = document['val'][i]
			if(rec['pop'] > 0):
				populationSize.append(rec['pop'])
				zeroToN.append(i)

	trace = go.Scatter(x = zeroToN,y = populationSize)
	data = [trace]
	plotly.plotly.iplot(data, filename=sys.argv[1])

if __name__ == "__main__":
    main()
