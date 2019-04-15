#=============================================AI==================================================
# Expectimax Maximization & Evaluation Functions
# AI Concepts from https://www.youtube.com/watch?v=l-hh51ncgDI
# ML concepts from https://www.youtube.com/watch?v=bVQUSndDllU&list=PLFt_AvWsXl0frsCrmv4fKfZ2OQIwoUuYO&index=1
# 2048 Algorithm from https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
#==================================================================================================
import random, string, copy, math, os, sys
import numpy as np
import pandas as pd
import torch
from tkinter import *
from tkinter import ttk
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#################################################
# HW10 SOLO PROBLEM (@print2DListResult)
#################################################

def print2DListResult(f):
#decorator: return a readable format for 2d lists only, otherwise do not print
    def print2d(*args):
        myList = f(*args)
        if isinstance(myList, list) and isinstance(myList[0], list):
            for row in range(len(myList)):
                print(' ', myList[row])
        return myList
    return print2d

#====================================4 move left+right algorithms=====================================
#@print2DListResult
def moveLeft(board, rows, cols):
    #only for mergeing
    for row in range(rows):
        for col in range(cols-1): #avoid "out of index" error, 1,2,3
            shiftLeft(board, row)
            curNum = board[row][col]
            nextNum = board[row][col+1]
            if curNum == nextNum:
                board[row][col] *= 2
                board[row][col+1] = 0
        shiftLeft(board, row)
    return board

def shiftLeft(board, row):
    # shift after merging everything in a row, AVOID DESTRUCTIVELY MODIFYING THE LIST!
    # otherwise would skip 0s, so [2,0,0,2] would not work
    curRow = board[row]
    shiftCount = curRow.count(0) #only do it as many times as how many 0's are in this row
    index = 0
    count = 0
    while index < len(curRow) and count < shiftCount:
        if curRow[index] == 0:
            curRow.pop(index)
            curRow.append(0)
            count += 1
        else:
            index += 1

#@print2DListResult  
def moveRight(board, rows, cols):
    #only for mergeing
    for row in range(rows):
        for col in range(cols-1, 0, -1): #avoid "out of index" error, so 3,2,1
            shiftRight(board, row)
            curNum = board[row][col]
            nextNum = board[row][col-1]
            if curNum == nextNum:
                board[row][col] *= 2
                board[row][col-1] = 0
        shiftRight(board, row)
    return board

def shiftRight(board, row):
    curRow = board[row]
    shiftCount = curRow.count(0)
    index = -1
    count = 0
    while index > -len(curRow): # -1,-2,-3
        if curRow[index] == 0 and count < shiftCount:
            curRow.pop(index)
            curRow.insert(0, 0) # replace with a 0 at the beginning/left
            count += 1
        else:
            index -= 1
#====================================4 move up+down algorithms=====================================
#@print2DListResult
def moveUp(board, rows, cols):
    #only for mergeing
    for col in range(cols):
        for row in range(rows-1):
            shiftUp(board, col)
            curNum = board[row][col]
            nextNum = board[row+1][col]
            if curNum == nextNum:
                board[row][col] *= 2
                board[row+1][col] = 0
        shiftUp(board, col)
    return board
    
def shiftUp(board, col):
    curCol = []
    rows = len(board)
    for row in range(rows): # IMPORTANT note: need to transform cols to a row
        curCol += [ board[row][col] ]
    shiftCount = curCol.count(0) #only do it as many times as how many 0's are in this row
    index = 0
    count = 0
    while index < len(curCol) and count < shiftCount:
        if curCol[index] == 0:
            curCol.pop(index)
            curCol.append(0)
            count += 1
        else:
            index += 1
    for row in range(rows): #now slap the new list of col #s back to the board
        board[row][col] = curCol[row]

#@print2DListResult
def moveDown(board, rows, cols):
    for col in range(cols):
        for row in range(rows-1, 0, -1): #3,2,1 not including 0
            shiftDown(board, col)
            curNum = board[row][col]
            nextNum = board[row-1][col]
            if curNum == nextNum:
                board[row][col] *= 2
                board[row-1][col] = 0
        shiftDown(board, col)
    return board

def shiftDown(board, col):
    curCol = []
    rows = len(board)
    for row in range(rows):
        curCol += [ board[row][col] ]
    shiftCount = curCol.count(0) #only do it as many times as how many 0's are in this row
    index = -1
    count = 0
    while index > -len(curCol) and count < shiftCount: #-1,-2,-3
        if curCol[index] == 0:
            curCol.pop(index)
            curCol.insert(0, 0)
            count += 1
        else:
            index -= 1
    for row in range(rows): #now slap the new list of col #s back to the board
        board[row][col] = curCol[row]

#=================================use to generate a random number on one empty square=======================
def generateRandomNumber():
    numberChoices = [2,4]
    #this is a cheating way to creating random num with different %
    getPercentage = random.randint(1, 100) #randint is inclusive on both sides!
    if getPercentage <= 10: #out of 100, so 90% num is 2, 10%num is 4
        return numberChoices[1] #which is 4
    else:
        return numberChoices[0] #which is 2

def placeRandomNumber(board):
    rows = len(board)
    cols = len(board[0])
    newNum = generateRandomNumber()
    possibleChoices = []
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0: #meaning empty box
                possibleChoices += [(row, col)]
    finalRow, finalCol = random.choice(possibleChoices)
    board[finalRow][finalCol] = newNum
    return board

#=============================================check game state==============================================
def isGameOver(board):
    rows = len(board)
    cols = len(board[0])    
    postLeft = copy.deepcopy(board)
    postUp = copy.deepcopy(board)
    postRight = copy.deepcopy(board)
    postDown = copy.deepcopy(board)

    postLeft = moveLeft(postLeft, rows, cols)
    postUp = moveUp(postUp, rows, cols)
    postRight = moveRight(postRight, rows, cols)
    postDown = moveDown(postDown, rows, cols)

    if board == postLeft and board == postUp and \
        board == postRight and board == postDown:
        return True
    return False

##########################################################################################################
# Testing AI Code
##########################################################################################################

def highestNumLocation(board):
    #atm this is keeping the largest number at the top left
    rows = len(board)
    cols = len(board[0])
    topLeft = board[0][0]
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum > topLeft:
                return -1
    return 1

def emptySquares(board):
    #bonus to more empty squares to ENCOURAGE merging
    rows = len(board)
    cols = len(board[0])
    count = 1
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum == 0:
                count *= 4 # increase bonus by a ratio
    return count

# this heuristics idea is adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
def findMaxNum(board):
    # the lowest maxNum is guaranteed to be 2, which is > -1
    rows = len(board)
    cols = len(board[0])
    maxNum = -1
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum > maxNum:
                maxNum = curNum
    return maxNum

def monotinicity(board):
    # bonus for "pyramid" number structure from a corner, here top left
    bonus = 1
    rows = len(board)
    cols = len(board[0])
    maxNum = findMaxNum(board)
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            # SUPER IMPORTANT algorithmic thinking: check diagonals' multitude, no checking last 3 squares at the other diagonal
            if row + col == 1 and curNum == maxNum/2 and curNum != 0:
                bonus *= 2
            elif row + col == 2 and curNum == maxNum/4 and curNum != 0:
                bonus *= 1.5
            elif row + col == 3 and curNum == maxNum/8 and curNum != 0:
                bonus *= 1.3
            elif row + col == 4 and curNum == maxNum/16 and curNum != 0:
                bonus *= 1.1
    return bonus

# this heuristics idea is also adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
def smoothness(board):
    # bonus for having adjacent tiles in order to merge + continue playing
    bonus = 1
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            try:
                if (curNum != 0 and \
                    (board[row+1][col] == curNum or \
                    board[row-1][col] == curNum or \
                    board[row][col+1] == curNum or \
                    board[row][col-1] == curNum)):
                    bonus *= 2
            except:
                continue
    return bonus

def evaluation(board):
    # input variables from evaluation functions, so our x1,x2,x3, etc.
    xL = emptySquares(board)
    xES = highestNumLocation(board)
    xMono = monotinicity(board)
    xSmooth = smoothness(board)

    # first: parameters in our ML algorithm, will be improved with Reinforcement Learning in PyTorch
    wLocation = 10
    wEmptySquare = 1
    wMono = 0.5
    wSmooth = 1

    biase1 = 0
    biase2 = 0
    biase3 = 0
    biase4 = 0
    return wLocation*(xL + biase1) + wEmptySquare*(xES + biase2) + \
            wMono*(xMono + biase3) + wSmooth*(xSmooth + biase4)

# RL algorithm will allow us to adjust to better parameters
def expectiMax(board, rows, cols, depth, maxDepth=2):
    # use a real-time update board deep copy of the actual board: aiBoard
    if depth == 0:
        return evaluation(board)
    else:
        #copy a new board and place one random digit onto it
        newBoard = copy.deepcopy(board)
        # it is a choice whether to turn on randomized board or not
        #placeRandomNumber(newBoard)
        for treeBranch in range(4):
            # copies the same board after putting a random digit for all four moves/children boards
            postRandomBoard = copy.deepcopy(newBoard)
            if treeBranch == 0:
                moveUp(postRandomBoard, rows, cols)
                value1 = expectiMax(postRandomBoard, rows, cols, depth-1)
            elif treeBranch == 1:
                moveLeft(postRandomBoard, rows, cols)
                value2 = expectiMax(postRandomBoard, rows, cols, depth-1)
            elif treeBranch == 2:
                moveDown(postRandomBoard, rows, cols)
                value3 = expectiMax(postRandomBoard, rows, cols, depth-1)
            elif treeBranch == 3:
                moveRight(postRandomBoard, rows, cols)
                value4 = expectiMax(postRandomBoard, rows, cols, depth-1)
        # update alpha to the largest value from 4 moves
        maxValue = max(value1, value2, value3, value4)
        if depth == maxDepth:
            #this if statement will run only at top level
            dict = {value1: "Up",
                    value2: "Left",
                    value3: "Down",
                    value4: "Right"}
            return maxValue, dict[maxValue]
        #return this max value to the upper tree (return max to parent node)
        return maxValue
#print(expectiMax(board))