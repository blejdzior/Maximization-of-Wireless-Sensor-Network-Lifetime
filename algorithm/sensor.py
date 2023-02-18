# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:46:23 2023

@author: pozdro
"""


class Sensor:
    def __init__(self, x, y, _range, _id):
        self.id = _id
        self.x = x
        self.y = y
        self.range = _range
        self.targets_in_range = []
        self.lifetime = 0
        self.remaining_lifetime = 0
        
#sigma - a constant greater than the maximum number of sensing areas by all network sensors to avoid unrealistic negative sensors lifetimes
    def lifetime_calc(self, sigma):
        if len(self.targets_in_range) != 0:
           self.lifetime = sigma / len(self.targets_in_range)
           self.remaining_lifetime = sigma - len(self.targets_in_range)