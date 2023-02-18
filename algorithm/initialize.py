# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 00:18:40 2023

@author: pozdro
"""
from algorithm.target import Target
from algorithm.sensor import Sensor
import numpy as np


def initialize(sensor_count, sensor_range, target_count, ):

# for now sensors are distributed using uniform distribution
    sensors = []
    for k in range(sensor_count):
        x_cor = np.random.uniform(low=0, high=100)
        y_cor = np.random.uniform(low=0, high=100)
        sensor = Sensor(x_cor, y_cor, sensor_range, k)
        sensors.append(sensor)

#for now targets are distributed using uniform distribution
    targets = []
    while len(targets) < target_count:
        x_cor = np.random.uniform(low=0, high=100)
        y_cor = np.random.uniform(low=0, high=100)
        target = Target(x_cor, y_cor)
        find_sensors_in_range(sensors, target)
        #adding only targets with at least one sensor in range
        if len(target.sensors) != 0:    
            targets.append(target)
            

# sigma - a constant greater than the maximum number of sensing areas by all network sensors
# to avoid unrealistic negative sensors lifetimes
    sigma = target_count + 5    

# removing sensors that doesn't have any targets in range
# and calculating sensor lifetime
    for sensor in sensors:
        if len(sensor.targets_in_range) == 0:
            sensors.remove(sensor)
        else: 
            sensor.lifetime_calc(sigma)

    return targets, sensors


# finds targets in range for sensor  
def find_targets_in_range(targets, sensor):
        for target in targets:
            if pow(sensor.x - target.x, 2) + pow(sensor.y - target.y, 2) <= pow(sensor.range,2):
                sensor.targets_in_range.append(target)
                target.sensors.append(sensor)

# finds sensors in range for target
def find_sensors_in_range(sensors, target):
    for sensor in sensors:
        if pow(sensor.x - target.x, 2) + pow(sensor.y - target.y, 2) <= pow(sensor.range,2):
                sensor.targets_in_range.append(target)
                target.sensors.append(sensor)