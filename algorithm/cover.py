# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:46:44 2023

@author: pozdro
"""


class Cover:
    def __init__(self):
        self.sensors = []
        self.targets_covered = set([])
        self.lifetime = 0
        self.critical_target = 0


