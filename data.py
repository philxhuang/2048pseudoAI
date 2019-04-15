#==========================================================================================
# A very clumsy attemp to read and write data stored in csv files
# because I have tried hard to write cutomized data file in .npz and .pt but both gave trouble
# so I gave up and now use the old good csv--->but everything is a string so I need to convert everyhing
# resources from https://docs.python.org/3.6/library/csv.html#module-contents
# https://code.tutsplus.com/tutorials/how-to-read-and-write-csv-files-in-python--cms-29907
# and https://github.com/utkuozbulak/pytorch-custom-dataset-examples
#==========================================================================================
import random, string, copy, math, os, sys, csv
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import torch
#importing pyTorch's neural network object + optimizer
from torch import nn, optim
#import functions like ReLU and log softmax
import torch.nn.functional as F
from torchvision import datasets, transforms

# everything must be float/long data type
# IMPORTANT NOTEs: pytorch only takes 0-based labels, so last col is just
# 0=256, 1=512, 2=1024, 3=2048, 4=4096, 5=8192
data = [
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 0, '256'],
        [1000., 100., 50., 50., 1, '512'],
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 0, '256'],
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 1, '512'],
        [1000., 100., 50., 50., 2, '1024'],
        [1000., 100., 50., 50., 1, '512'],
        [1000., 100., 50., 50., 0, '256'],
        [1000., 100., 50., 50., 0, '256'],
        [1000., 100., 50., 50., 1, '512'],
        # first 14
        [100., 100., 50., 50., 2, '1024'],
        [100., 100., 50., 50., 1, '512'],
        [100., 100., 50., 50., 2, '1024'],
        [100., 100., 50., 50., 0, '256'],
        [100., 100., 50., 50., 1, '512'],
        [100., 100., 50., 50., 2, '1024'],
        [100., 100., 50., 50., 1, '512'],
        [100., 100., 50., 50., 1, '512']
        ]

def writeCSV():
    with open('data/data.csv', 'w', newline='') as dataFile:
        writer = csv.writer(dataFile)
        writer.writerows(data) 
    print("Writing complete")

# need to rewrite the csv file everytime we add new data
writeCSV()

def readCSV():
    with open('data/data.csv', newline='') as dataFile:
        reader = csv.reader(dataFile)
        for row in reader:
            print(row)

def customCSV(csvPath):
        dataset = pd.read_csv(csvPath, header=None)

        xLocation = np.asarray(dataset.iloc[:, 0])
        xEmptySquare = np.asarray(dataset.iloc[:, 1])
        xMono = np.asarray(dataset.iloc[:, 2])
        xSmooth = np.asarray(dataset.iloc[:, 3])

        parameters = []
        for row in range(len(xLocation)):
            parameters.append([xLocation[row], xEmptySquare[row], xMono[row], xSmooth[row] ])
        parameters = np.array(parameters)

        # Second column is the labels, datatype: numpy array, float
        labels = np.asarray(dataset.iloc[:, 4])
        #print(labels)
        
        return dataset, parameters, labels

#dataset, parameters, labels = customCSV('data/data.csv')
