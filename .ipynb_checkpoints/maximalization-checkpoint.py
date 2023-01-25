import numpy as np
import math
import inspect
import random


class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sensors = []

    def __len__(self):
        return len(self.sensors)


class Sensor:
    def __init__(self, x, y, _range, battLife, _id):
        self.id = _id
        self.x = x
        self.y = y
        self.range = _range
        self.battLife = battLife
        self.targetsInRange = []
        self.lifetime = 0
        self.remainingLifetime = 0


class Cover:
    def __init__(self):
        self.sensors = []
        self.targetsCovered = set([])
        self.lifetime = 0
        self.criticalTarget = 0


class Network:
    def __init__(self):
        self.sensors = [] # Chromosome
        
        self.covers = [] # Count of covers - fitness function 1
        self.overlap = 0
        self.variance = 0
# DF - difference factor, for more info see: https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-wss.2017.0069 section 3.5
        self.DF = 0 # fitness function 2

    def __len__(self):
        return len(self.covers)

    def calculateDF(self):
        sumCritSensorsLifetime = 0
        sumRemainingSensorLifetime = 0
        for cover in self.covers:
            sumCritSensorsLifetime += max(cover.criticalTarget.sensors, key = lambda x: x.remainingLifetime).remainingLifetime
            sumRemainingSensorLifetime += min(cover.sensors, key = lambda x: x.remainingLifetime).remainingLifetime
        if len(self.covers) == 0:
            self.DF = 0
        else:
            self.DF = (sumCritSensorsLifetime - sumRemainingSensorLifetime)/len(self.covers)

            
            

def initialize(sensorCount, sensorDist,sensorRange, battLife, targetCount, targetDist  ):
# for now sensors are distributed using uniform distribution
    sensors = []
    for i in range(sensorCount):
        x_cor = np.random.uniform(low=0, high=100)
        y_cor = np.random.uniform(low=0, high=100)
        sensors.append(Sensor(x_cor,y_cor,sensorRange, battLife, i))
        
#for now targets are distributed using uniform distribution
    targets = []
    for i in range(targetCount):
        x_cor = np.random.uniform(low=0, high=100)
        y_cor = np.random.uniform(low=0, high=100)
        targets.append(Target(x_cor, y_cor))
            
    findTargetsInRange(targets, sensors)

    sigma = targetCount + 5
    sensorLifeTimecalc(sensors, sigma)
    
    return targets, sensors
    
def findTargetsInRange(targets, sensors):
    #finding targets in range for each sensor
    for sensor in sensors:
        for target in targets:
            if pow(sensor.x - target.x, 2) + pow(sensor.y - target.y, 2) <= pow(sensor.range,2):
                sensor.targetsInRange.append(target)
                target.sensors.append(sensor)
                
#sigma - a constant greater than the maximum number of sensing areas by all network sensors to avoid unrealistic negative sensors lifetimes
def sensorLifeTimecalc(sensors, sigma):
    for sensor in sensors:
        if len(sensor.targetsInRange) != 0:
            sensor.lifetime = sigma / len(sensor.targetsInRange)
            sensor.remainingLifetime = sigma - len(sensor.targetsInRange)
        
#critical target is a target with the least amount of sensors covering it
def findCriticalTarget(targets):
    critTarget = min(targets, key=len)
    return critTarget
        
        
#upperLimit = number of sensors covering critical target
def sensorCollectionforNetwork(sensors, targets, upperLimit):
    random.shuffle(sensors)
    network = Network()
    i = 0

    while len(network) <= upperLimit and i < len(sensors):    
        cover = Cover()
        while len(cover.targetsCovered) != len(targets) and i < len(sensors):
            if len(sensors[i].targetsInRange): 
                cover.sensors.append(sensors[i])
                cover.targetsCovered.update(sensors[i].targetsInRange)
            i = i + 1
        if len(cover.targetsCovered) == len(targets):
            cover.lifetime = min(cover.sensors, key=lambda x: x.lifetime).lifetime
            cover.criticalTarget = findCriticalTarget(cover.targetsCovered)
            covers.append(cover)
    network.calculateDF()

    return network



targets, sensors = initialize(1000, 0, 7, 100, 20, 0)

inspect.getmembers(sensors[0])
criticalTarget = findCriticalTarget(targets)
print(criticalTarget.sensors)
# inspect.getmembers(criticalTarget)
network = sensorCollectionforNetwork(sensors, targets, len(findCriticalTarget(targets).sensors))

max_population = 10
networks = []
for i in range(max_population):
    networks.append(sensorCollectionforNetwork(sensors,targets,len(findCriticalTarget(targets).sensors))


                    
                    
print(network.DF)
print(len(network.covers))
# inspect.getmembers(network)

# i = 0
# for sensor in sensors:
#     print(str(i) + " :")
#     print("x: " + str(sensor.x))
#     print("y: " + str(sensor.y))
#     print("range: " + str(sensor.range))
#     i = 1 + i
#     for target in sensor.targetsInRange:
#         print("target: " +  str(target.x) , str(target.y))
#         for sensor in target.sensors:
#             print("sensor for target: " + str(sensor.x), str(sensor.y))
        


