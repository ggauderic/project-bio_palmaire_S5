# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:16:58 2023

@author: 33649
"""


import numpy as np
import matplotlib.pyplot as plt



ax = plt.gca()
ax.set_facecolor((2/255,14/255,26/255)) #(2,14,26)

x = np.linspace(-2, 2, 10)
y = np.exp(-x)

plt.plot(x, y, color="lightblue") #(2, 147, 178)

plt.show()