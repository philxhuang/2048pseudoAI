#=============================================AI==================================================
# Data Visualizable for Preliminary Testing
# Sourced from https://matplotlib.org/index.html
# Pie Chart from https://matplotlib.org/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
#==================================================================================================
import random, string, copy, math, os, sys, csv
import numpy as np
from tkinter import *
from tkinter import ttk
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# partially learned from https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray-in-python
# and from https://www.w3resource.com/graphics/matplotlib/piechart/matplotlib-piechart-exercise-2.php
def drawPie(isExpectimax, isMinimax, isRL):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    if isExpectimax:
        highestTiles, depths, moveCounts, isEvilMode, rows, cols, baseNum, baseProb = customCSV('data/expectimax.csv')
    elif isMinimax:
        highestTiles, depths, moveCounts, isEvilMode, rows, cols, baseNum, baseProb = customCSV('data/minimax.csv')
    elif isRL:
        highestTiles, depths, moveCounts, isEvilMode, rows, cols, baseNum, baseProb = customCSV('data/RL.csv')
    labels = ["256", "512", "1024", "2048", "4096"]
    sizes = [highestTiles.count(256), highestTiles.count(512), 
                highestTiles.count(1024), highestTiles.count(2048), highestTiles.count(4096)]
    #print(sizes)
    explode = (0, 0, 0, 0.1, 0)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    if isExpectimax:
        plt.title("Expectimax Performance at Depth = "+str(depths[0])+" When Evil Mode is "+str(isEvilMode[0]))
    elif isMinimax:
        plt.title("Minimax Performance at Depth = "+str(depths[0])+" When Evil Mode is "+str(isEvilMode[0]))
    elif isRL:
        plt.title("Reinforcement-Learning Performance at Depth = "+str(depths[0])+" When Evil Mode is "+str(isEvilMode[0]))

    plt.show()

# learned from https://stackoverflow.com/questions/13203868/how-to-write-to-csv-and-not-overwrite-past-text
def writeCSV(highestTile, depth, moveCount, isEvilMode, rows, cols, baseNum, baseProb, isExpectimax, isMinimax, isRL): 
    # append new values to new rows in one of the three files
    if isExpectimax:
        with open('data/expectimax.csv', 'a', newline='') as dataFile:
            writer = csv.writer(dataFile)
            writer.writerow([highestTile, depth, moveCount, isEvilMode, rows, cols, baseNum, baseProb])
    elif isMinimax:
        with open('data/minimax.csv', 'a', newline='') as dataFile:
            writer = csv.writer(dataFile)
            writer.writerow([highestTile, depth, moveCount, isEvilMode, rows, cols, baseNum, baseProb])
    elif isRL:
        with open('data/RL.csv', 'a', newline='') as dataFile:
            writer = csv.writer(dataFile)
            writer.writerow([highestTile, depth, moveCount, isEvilMode, rows, cols, baseNum, baseProb])

# also learned from https://stackoverflow.com/questions/13203868/how-to-write-to-csv-and-not-overwrite-past-text
def readCSV(isExpectimax, isMinimax, isRL):
    if isExpectimax:
        with open('data/expectimax.csv', newline='') as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                print(row)
    elif isMinimax:
        with open('data/minimax.csv', newline='') as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                print(row)
    elif isRL:
        with open('data/RL.csv', newline='') as dataFile:
            reader = csv.reader(dataFile)
            for row in reader:
                print(row)

def customCSV(csvPath):
    dataset = pd.read_csv(csvPath, header=None)

    highestTiles = np.asarray(dataset.iloc[:, 0])
    highestTilesList = []
    for tile in highestTiles:
        highestTilesList.append(tile)

    depths = np.asarray(dataset.iloc[:, 1])
    moveCounts = np.asarray(dataset.iloc[:, 2])

    isEvilMode = np.asarray(dataset.iloc[:, 3])
    rows = np.asarray(dataset.iloc[:, 4])
    cols = np.asarray(dataset.iloc[:, 5])
    baseNum = np.asarray(dataset.iloc[:, 6])
    baseProb = np.asarray(dataset.iloc[:, 7])
        
    return highestTilesList, depths, moveCounts, isEvilMode, rows, cols, baseNum, baseProb
