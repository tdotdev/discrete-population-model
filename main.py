import time
import copy
import plotly
plotly.tools.set_credentials_file(username='timothyCSnyder', api_key='mZ5dCnoJSLQ8CSq297Hc')
import numpy as np
import plotly.graph_objs as go

class PopulationModel:
    def __init__(self, initPopulation, initCapacity, alpha, amplitude):
        self.population = initPopulation
        self.alpha = alpha;
        self.capacity = initCapacity
        self.initCapacity = initCapacity
        self.amplitude = amplitude
        self.t = 0
        

    def step(self):
        self.capacity = self.initCapacity + (self.amplitude * pow(-1, self.t))
        self.t = self.t + 1;
        self.population = self.alpha * self.population * (1 - ((self.alpha - 1) / self.alpha) * self.population / self.capacity)


n = 1000;
series = []
model = PopulationModel(.5, 1, 1.7, .1)
i = 0

print("Start population: " + str(model.population))

start_time = time.time()

while(i != n):
    series.append(copy.deepcopy(model))
    model.step()
    i = i + 1;
end_time = time.time()


print("End population: " + str(model.population))
print("Time: " + str(end_time - start_time) + "s")
print(len(series))

x_data = []
y_data = []

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





    


    
