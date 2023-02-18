# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:44:39 2023

@author: pozdro
"""

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sensors = []

    def __len__(self):
        return len(self.sensors)

