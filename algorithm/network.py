# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:19:47 2023

@author: pozdro
"""
from algorithm.cover import Cover

class Network:
    
    def __init__(self, sensors = None):
        if sensors is None:
            self.sensors = []
        else:    
            self.sensors = sensors # Chromosome
        
        self.covers = [] # Count of covers - fitness function 1
        
        # DF - difference factor, for more info see: https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-wss.2017.0069 section 3.5
        # initializing with unrealistic high value
        self.DF = 1000 # fitness function 2


    def __len__(self):  
        return len(self.covers)


    def calculateDF(self):
        sum_crit_sensors_lifetime = 0
        sum_remaining_sensor_lifetime = 0
        if len(self.covers) != 0:
            for cover in self.covers:
                sum_crit_sensors_lifetime += max(cover.critical_target.sensors, key = lambda x: x.remaining_lifetime).remaining_lifetime
                sum_remaining_sensor_lifetime += min(cover.sensors, key = lambda x: x.remaining_lifetime).remaining_lifetime
            self.DF = (sum_crit_sensors_lifetime - sum_remaining_sensor_lifetime)/len(self.covers)
    
            
    #critical target is a target with the least amount of sensors covering it
    def find_critical_target(self, targets):
        crit_target = min(targets, key=len)
        return crit_target
            
            
 
    # collects sensors into covers in order-based manner 
    def sensor_collection(self, targets):
        i = 0
        # upper_Limit = number of sensors covering critical target
        upper_limit = len(self.find_critical_target(targets).sensors)
        
        while len(self.covers) < upper_limit and i < len(self.sensors):    
            cover = Cover()
            while len(cover.targets_covered) != len(targets) and i < len(self.sensors):
                if len(self.sensors[i].targets_in_range): 
                    cover.sensors.append(self.sensors[i])
                    cover.targets_covered.update(self.sensors[i].targets_in_range)
                i = i + 1
            if len(cover.targets_covered) == len(targets):
                cover.lifetime = min(cover.sensors, key=lambda x: x.lifetime).lifetime
                cover.critical_target = self.find_critical_target(cover.targets_covered)
                self.covers.append(cover)


