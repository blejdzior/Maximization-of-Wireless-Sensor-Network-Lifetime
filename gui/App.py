# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:22:33 2023

@author: pozdro
"""
from functools import partial
import tkinter as tk
from tkinter import ttk, Text
from algorithm.algorithm import calculate
import numpy as np

from pymoo.visualization.scatter import Scatter
from pymoo.visualization.heatmap import Heatmap

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Maximalization')
        self.create_widgets()


    def create_widgets(self):
     
        self.frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, columnspan=2, rowspan=10)
        # self.frame.grid_propagate(False)
        # number of sensors input
        # %P sets it so validation is called for new input
        # partial function is passed
        check_input_wrapper = (self.register(partial(check_input_int, upper_bound=1000, lower_bound=0)), '%P')     
        
        ttk.Label(self.frame,text='Sensor count: ').grid(row=0, column=0, padx=5, pady=5)
        self.sensor_count = ttk.Entry(self.frame, validate='key', validatecommand=check_input_wrapper)
        self.sensor_count.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        check_input_wrapper_2 = (self.register(partial(check_input_int, upper_bound=10, lower_bound=0)), '%P')
        ttk.Label(self.frame,text='Sensor range: ').grid(row=2, column=0, padx=5, pady=5)
        self.sensor_range = ttk.Entry(self.frame, validate='key', validatecommand=check_input_wrapper_2)
        self.sensor_range.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Label(self.frame,text='Target count: ').grid(row=4, column=0, padx=5, pady=5)
        self.target_count = ttk.Entry(self.frame, validate='key', validatecommand=check_input_wrapper)
        self.target_count.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        

        ttk.Label(text='Result: [number of covers, difference factor]').grid(row=2, column=8, padx=5, pady=5)
        self.text = Text()
        self.text.grid(row=3, column=8, padx=5, pady=5)
        
        # using partial just to get it working lol
        button = ttk.Button(self.frame, text='Calculate', command=partial(self.button_handler, self))
        button.grid(row=10, column=0, padx=5, pady=5)
        
        

        
    def button_handler(self, event):
        self.text.delete(1.0, tk.END) 


        sensor_range = int(self.sensor_range.get())
        sensor_count = int(self.sensor_count.get())
        target_count = int(self.target_count.get())
        # print(distribution)
        print(sensor_range)
        print(sensor_count)
        print(target_count)
        res = calculate(sensor_count, sensor_range, target_count)
        print(res)
        print(res.F)
        print(res.X)
        print(res.X[0])
        Scatter().add(res.F).save('scatter.png')
        plot = tk.PhotoImage(file="scatter.png")
        self.text.image_create(1.0, image=plot)
        string = np.array2string(res.F)
        self.text.insert('end', '\n')
        self.text.insert('end', string)
        
        
        
def check_input_int(newval, upper_bound, lower_bound):
    try:
        integer_result = int(newval)
    except ValueError:
        if(newval == ''):
            return True
        else:
            return False
    else:
        return integer_result <= upper_bound and integer_result > lower_bound
