#=============================================================================
# PyTorch learned from Udacity AI courses for free
# also learned from notebook from this github resources made by Udacity courses
# https://github.com/udacity/deep-learning-v2-pytorch/blob/master/intro-to-pytorch/Part%201%20-%20Tensors%20in%20PyTorch%20(Exercises).ipynb
#=============================================================================
import random, string, copy, math, os, sys
import numpy as np
import pandas as pd
import torch
#importing pyTorch's neural network object + optimizer
from torch import nn, optim
#import functions like ReLU and log softmax
import torch.nn.functional as F
from torchvision import datasets, transforms

def activation(x):
    #transform a number into probability between 0 and 1
    return 1/(1+torch.exp(-x))

class network(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        #flatten the input tensor
        x = x.view(x.shape[0], -1)
        return x

model = network()
criterion = nn.NLLLoss()
#the Atom optimizer uses the concept of momentum to optimize gradient descent, lr=learning rate
optimizer = optim.Adam(model.parameters(), lr=0.003)

epochs = 5
for e in range(epochs):
    loss = 0
    for _, labels in trainloader:
        logps = model(_)
        loss = criterion(logps, labels)

        #reset gradient for training so it won't cumulate and mess up training
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss += loss.item()
    print(f"Traning loss: {loss}")