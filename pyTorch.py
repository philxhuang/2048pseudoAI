#=============================================================================
# PyTorch learned from Udacity AI courses for free
# also learned from notebook from this github resources made by Udacity courses
# https://github.com/udacity/deep-learning-v2-pytorch/blob/master/intro-to-pytorch/Part%201%20-%20Tensors%20in%20PyTorch%20(Exercises).ipynb
#=============================================================================
import random, string, copy, math, os, sys
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
# import the csv data read from data.py
from data import customCSV

#=============================================important functions for reference===================================
def activation(x):
    #transform a number into probability between 0 and 1, sigmoid activation
    return 1/(1+torch.exp(-x))

def softmax(x):
    #calculate the probability by using exponentials
    return torch.exp(x)/torch.sum(torch.exp(x), dim=1).view(-1, 1)

def basicTestNN():
    #the features here are actually weights from the eval function from ai.py
    features = torch.tensor([ [1000., 100., 50., 50.] ])
    inputUnits = features.shape[1] # 4 in this case

    hiddenUnits = 2
    outputUnits = 1 

    #create weight matrices that match the results of matrix calculations
    w1 = torch.randn(inputUnits, hiddenUnits) # 4 by 2
    w2 = torch.randn(hiddenUnits, outputUnits) # 2 by 1

    #create a single 1 by 1 bias matrix/2dList
    bias1 = torch.randn((1, hiddenUnits)) # 1 by 2
    bias2 = torch.randn(1, outputUnits) # 1 by 1

    # calculate the probability Y with sigmoid activation function
    # mm = matmul ---> matrix multiplication, only more strict
    h = activation(torch.mm(features, w1) + bias1)
    y = activation(torch.mm(h, w2) + bias2)
    print(y)

#=======================================actual nn model===========================================
# dataset is a big 2dList with both parameters and labels, details see data.py
# parameter--->2d list, each row for 4 parameters in a list
# labels--->1d list, scalar data for the max square achieved
dataset, parameters, labels = customCSV('data/data.csv')

class network(nn.Module):
    def __init__(self):
        super().__init__()
        self.inputUnits = 4
        self.hiddenUnits = 2
        self.outputUnits = 1 
        # inputs to hidden layer, linear transformation
        self.hidden = nn.Linear(self.inputUnits, self.hiddenUnits)
        # output layer, 10 units, 1 for each digit
        self.output = nn.Linear(self.hiddenUnits, self.outputUnits)

    def forward(self, x):
        # x go through the operations, pass through later and then transfer
        # hidden layer with sigmoid activation
        x = F.sigmoid(self.hidden(x))
        # output layer with softmax activation
        x = F.softmax(self.output(x))
        return x

def runNN(dataset, parameters, labels):
    # loading numpy array data and run loss NN to train and find the best parameters
    #print(type(parameters[0]), type(labels[0]))

    # 1st arg excepts scalar float, 2nd arg expects scalar long (data type)
    trainSet = torch.utils.data.TensorDataset(torch.FloatTensor(parameters), torch.LongTensor(labels))
    trainLoader = torch.utils.data.DataLoader(trainSet, batch_size=10, shuffle=True)

    model = nn.Sequential(nn.Linear(4, 2),
                      nn.ReLU(),
                      nn.Linear(2, 1),
                      nn.LogSoftmax(dim=1))
    # Define the loss
    criterion = nn.NLLLoss()

    # Get one batch of data
    parameterSet, labels = next(iter(trainLoader))

    # Flatten parameters
    parameterSet = parameterSet.view(parameterSet.shape[0], -1)
    #print(parameterSet)

    # Forward pass, get our log-probabilities
    output = model(parameterSet)
    #print(output)
            
    loss = criterion(output, labels)

    print(f"Training loss: {loss}")

runNN(dataset, parameters, labels)
