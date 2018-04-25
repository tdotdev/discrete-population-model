class TimeModel:
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