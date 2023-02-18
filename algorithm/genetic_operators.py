# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:47:35 2023

@author: pozdro
"""
import random
import numpy as np
from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from algorithm.network import Network


class MySampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        X = np.full((n_samples, 1), None, dtype=object)
        

        for i in range(n_samples):
            # random 
            sensors = random.sample(problem.sensors, len(problem.sensors))
            X[i, 0] = Network(sensors)
        return np.array(X)
            

class MyCrossover(Crossover):
    def __init__(self):
        
        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)
    
    def _do(self, problem, X, **kwargs):    
        #  input shape: (n_parents, n_matings, n_var)
        n_parents, n_matings, n_var = X.shape
        
        # Because there's equal number of parents and offsprings result keeps shape of X
        Y = np.full_like(X, None, dtype=object)
        
        #for each mating provided
        for k in range(n_matings):
            #get the parents
            a, b = X[0,k,0], X[1,k,0]
            
            #prepare the offsprings
            off_a = Network()
            off_b = Network()
            
            #Cutoff points - sensors of parent 1 to the left of cutting point will be copied to offspring
            # then rest of sensors from parent 2 will be copied (exluding duplicates)
            cutoff_a = random.randrange( len(a.sensors))
            cutoff_b = random.randrange( len(b.sensors))
            off_a.sensors = a.sensors[:cutoff_a]
            off_b.sensors = b.sensors[:cutoff_b]
            
            for sensor in b.sensors:
                if sensor in off_a.sensors:
                    continue
                else:
                    off_a.sensors.append(sensor)
                    
            for sensor in a.sensors:
                if sensor in off_b.sensors:
                    continue
                else:
                    off_b.sensors.append(sensor)
            
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
                    
                    #the swap
                    X[i,0].sensors[id1], X[i,0].sensors[id2] = X[i,0].sensors[id2],  X[i,0].sensors[id1]
                
        return X
    
        
class MyDuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        return a.X[0].sensors == b.X[0].sensors

    
    

    
    