#=============================================AI==================================================
# Data Visualizable for Preliminary Testing
# Sourced from https://matplotlib.org/index.html
# Pie Chart from https://matplotlib.org/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
#==================================================================================================
import random, string, copy, math, os, sys
import numpy as np
import pandas as pd
import torch
from tkinter import *
from tkinter import ttk
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = "64", "128", "256", "512", "1024", "2048"
sizes = [0, 1, 3, 3, 4, 0]
explode = (0, 0, 0, 0, 0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
