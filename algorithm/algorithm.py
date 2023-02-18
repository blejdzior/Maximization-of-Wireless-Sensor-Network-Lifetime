# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:47:57 2023

@author: pozdro
"""
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from algorithm.genetic_operators import MyDuplicateElimination, MyMutation, MyCrossover, MySampling
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.selection.rnd import RandomSelection
from algorithm.initialize import initialize

class MyProblem(ElementwiseProblem):
    def __init__(self, sensors, targets):
        super().__init__(n_var = 1, n_obj=2, n_ieq_constr=0)
        self.sensors = sensors
        self.targets = targets
        
    def _evaluate(self, X, out, *args, **kwargs):
        res = []
        for network in X:
            # collect sensors into covers
            network.sensor_collection(self.targets)
            
            # Number of covers in network -- first goal
            # (needs to be maximized so minimizing negative value)
            F1 = -len(network) 
            
            network.calculateDF()
            F2 = network.DF # DF -- second goal - minimized
            res.append([F1, F2])
        out['F'] = np.array(res)


def calculate(sensor_count, sensor_range, target_count):
    targets, sensors = initialize(sensor_count, sensor_range, target_count)
    
    algorithm = NSGA2(pop_size=100,
                      sampling=MySampling(),
                      crossover=MyCrossover(),
                      mutation=MyMutation(),
                      eliminate_duplicates=MyDuplicateElimination(),
                      selection=RandomSelection())
    
    res = minimize(MyProblem(sensors, targets),
                   algorithm,
                   ('n_gen', 100),
                   seed=1,
                   verbose=False)
    
    # reversing number of covers so it's positive
    for result in res.F:
        result[0] = -result[0]
    return res
    



    