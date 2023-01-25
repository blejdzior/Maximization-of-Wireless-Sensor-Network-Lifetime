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
    def __init__(self, sensors):
        self.sensors = sensors # Chromosome
        
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
    covers = []
    i = 0

    while len(covers) <= upperLimit and i < len(sensors):    
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

    return covers



from pymoo.core.problem import ElementwiseProblem
from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.duplicate import ElementwiseDuplicateElimination

class MyProblem(ElementwiseProblem):
    def __init__(self, sensors, targets, upperLimit):
        super().__init__(n_var = 1, n_obj=2, n_ieq_constr=0)
        self.sensors = sensors
        self.targets = targets
        self.upperLimit = upperLimit
        
    def _evaluate(self, networks, out, *args, **kwargs):
        res = []
        for network in networks:
            network.covers = sensorCollectionforNetwork(network.sensors, self.targets, self.upperLimit)
            F1 = -len(network) # Number of covers in network -- first goal (needs to be maximized so minimizing negative value)
            network.calculateDF()
            F2 = network.DF # DF -- second goal - minimized
            res.append([F1, F2])
        out['F'] = np.array(res)


class MySampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        X = np.full((n_samples, 1), None, dtype=object)
        

        for i in range(n_samples):
            sensors = random.sample(problem.sensors, len(problem.sensors))
            X[i, 0] = Network(sensors)
        return np.array(X)
            

class MyCrossover(Crossover):
    def __init__(self):
        
        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)
    
    def _do(self, problem, X, **kwargs):
        
        # The input of has the following shape (n_parents, n_matings, n_var)
        n_parents, n_matings, n_var = X.shape
        
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)
        
        #for each mating provided
        for k in range(n_matings):
            #get the parents
            a, b = X[0,k,0], X[1,k,0]
            
            #prepare the offsprings
            off_a_sensors = []
            off_b_sensors = []
            
            #Cutoff points - sensors of parent 1 to the left of cutting point will be copied to offspring
            # then rest of sensors from parent 2 will be copied (exluding duplicates)
            cutoff_a = random.randrange( len(a))
            cutoff_b = random.randrange( len(b))
            off_a_sensors = a.sensors[:cutoff_a]
            off_b_sensors = b.sensors[:cutoff_b]
            for sensor in b.sensors:
                if sensor in off_a_sensors:
                    continue
                else:
                    off_a_sensors.append(sensor)
            for sensor in a.sensors:
                if sensor in off_b_sensors:
                    continue
                else:
                    off_b_sensors.append(sensor)
            off_a = Network(off_b_sensors)
            off_b = Network(off_a_sensors)
            
            Y[0, k, 0], Y[1, k, 0] = off_a, off_b
        return Y
        
        
        
class MyMutation(Mutation):
    def __init__(self):
        super().__init__()
    
    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
                n_swapes = random.randint(1, len(X[i,0].sensors))
                for k in range(n_swapes):
                    id1 = random.randrange(len(X[i,0].sensors))
                    id2 = random.randrange(len(X[i,0].sensors))
                    gene1_copy = X[i,0].sensors[id1]
                    X[i,0].sensors[id1] = X[i,0].sensors[id2]
                    X[i,0].sensors[id2] = gene1_copy
        return X
    
        
class MyDuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        return a.X[0].sensors == b.X[0].sensors



    
    
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
 
    
targets, sensors = initialize(1000, 0, 7, 100, 20, 0)

inspect.getmembers(sensors[0])
criticalTarget = findCriticalTarget(targets)

algorithm = NSGA2(pop_size=30,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())

res = minimize(MyProblem(sensors, targets, len(criticalTarget.sensors)),
               algorithm,
               ('n_gen', 100),
               seed=1,
               verbose=False)
               

    
from pymoo.visualization.scatter import Scatter
Scatter().add(res.F).show()
res.F
res.X
print(criticalTarget.sensors)

# inspect.getmembers(criticalTarget)

# #(self, x, y, _range, battLife, _id)
# sensor1 = Sensor(10,10, 1, 1, 1)
# sensor2 = Sensor(11,11, 1, 1, 2)
# sensor3 = Sensor(12,12, 1, 1, 3)
# sensor4 = Sensor(13,13, 1, 1, 4)
# sensors = []
# sensors.append(sensor1)
# sensors.append(sensor2)
# sensors.append(sensor3)
# sensors.append(sensor4)

# network1 = Network(sensors)
# sensors1 =  random.sample(sensors, len(sensors))
# network2 = Network(sensors1)
# network1.sensors == network2.sensors
# network = sensorCollectionforNetwork(sensors, targets, len(findCriticalTarget(targets).sensors))
              
                    
# print(network.DF)
# print(len(network.covers))
# inspect.getmembers(network)

for k in range(len(res.X)):
    print("NETWORK: " + str(k))
    j = 0
    
    for cover in res.X[k][0].covers:
        print("  " + "COVER: " + str(j) +": ")
        i = 0
        j = j+1
        for sensor in cover.sensors:
            print("    " + str(i) + ": ")
            print("     x: " + str(sensor.x))
            print("     y: " + str(sensor.y))
            print("     range: " + str(sensor.range))
            i = 1 + i
            # for target in sensor.targetsInRange:
        #     print("  target: " +  str(target.x) , str(target.y))
        #     for sensor in target.sensors:
        #         print("  sensor for target: " + str(sensor.x), str(sensor.y))



