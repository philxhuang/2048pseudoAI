#=============================================AI==================================================
# Expectimax Maximization & Evaluation Functions
# AI Concepts from https://www.youtube.com/watch?v=l-hh51ncgDI
# ML concepts from https://www.youtube.com/watch?v=bVQUSndDllU&list=PLFt_AvWsXl0frsCrmv4fKfZ2OQIwoUuYO&index=1
# 2048 Algorithm from https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
#==================================================================================================
import random, string, copy, math, os, sys
import numpy as np
from tkinter import *
from tkinter import ttk

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
def moveLeft(board, rows, cols, baseNum):
    #only for mergeing
    for row in range(rows):
        for col in range(cols-1): #avoid "out of index" error, 1,2,3
            shiftLeft(board, row)
            curNum = board[row][col]
            nextNum = board[row][col+1]
            if curNum == nextNum:
                board[row][col] *= baseNum
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
def moveRight(board, rows, cols, baseNum):
    #only for mergeing
    for row in range(rows):
        for col in range(cols-1, 0, -1): #avoid "out of index" error, so 3,2,1
            shiftRight(board, row)
            curNum = board[row][col]
            nextNum = board[row][col-1]
            if curNum == nextNum:
                board[row][col] *= baseNum
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
def moveUp(board, rows, cols, baseNum):
    #only for mergeing
    for col in range(cols):
        for row in range(rows-1):
            shiftUp(board, col)
            curNum = board[row][col]
            nextNum = board[row+1][col]
            if curNum == nextNum:
                board[row][col] *= baseNum
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
def moveDown(board, rows, cols, baseNum):
    for col in range(cols):
        for row in range(rows-1, 0, -1): #3,2,1 not including 0
            shiftDown(board, col)
            curNum = board[row][col]
            nextNum = board[row-1][col]
            if curNum == nextNum:
                board[row][col] *= baseNum
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

#=============================================check game state==============================================
def isGameOver(realBoard, baseNum):
    board = copy.deepcopy(realBoard)
    rows = len(board)
    cols = len(board[0])    
    postLeft = copy.deepcopy(board)
    postUp = copy.deepcopy(board)
    postRight = copy.deepcopy(board)
    postDown = copy.deepcopy(board)

    postLeft = moveLeft(postLeft, rows, cols, baseNum)
    postUp = moveUp(postUp, rows, cols, baseNum)
    postRight = moveRight(postRight, rows, cols, baseNum)
    postDown = moveDown(postDown, rows, cols, baseNum)

    if board == postLeft and board == postUp and \
        board == postRight and board == postDown:
        return True
    return False

##########################################################################################################
# Evaluation Functions for AI
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
                count *= 1.1 # increase bonus by a ratio
    return count

# this heuristics idea is adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
def findMaxNumAndPos(board):
    # the lowest maxNum is guaranteed to be 2, which is > -1
    targetRow = 0
    targetCol = 0

    rows = len(board)
    cols = len(board[0])
    maxNum = -1
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum > maxNum:
                maxNum = curNum
                targetRow = row
                targetCol = col
    return maxNum, targetRow, targetCol

# ideas refined by https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def monotinicity(board):
    # bonus for making rows/cols either strictly decreasing from the left cornor
    bonus = 1
    rows = len(board)
    cols = len(board[0])
    # for every row, check if strictly decreasing from left to right
    for row in range(rows):
        temp = 1
        for col in range(cols-1):
            curNum = board[row][col]
            nextNum = board[row][col+1]
            if curNum > nextNum:
                temp = 1.5
            else:
                temp = 1
        bonus *= temp
    #for every col, check if strictly decreasing from up to down
    for col in range(cols):
        temp = 1
        for row in range(rows-1):
            curNum = board[row][col]
            nextNum = board[row+1][col]
            if curNum > nextNum:
                temp = 1.5
            else:
                temp = 1
        bonus *= temp
    return bonus

# this heuristics idea is also adopted from:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
# idea refined by https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def smoothness(board):
    # measures the difference between neighboring tiles and tries to minimize this count
    score = 1
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(0, cols, 2): # skip a col because we already check all 4 adjacent tiles, more efficient
            curNum = board[row][col]
            for r,c in [(0,1),(1,0),(0,-1),(-1,0)]:
                if rows > row+r >= 0 and cols > col+c >= 0 and curNum != 0:
                    checkedNum = board[row+r][col+c]
                    if curNum-checkedNum != 0:
                        score += math.log(abs(curNum - checkedNum),10) # best way to make large differences small, by using log10
    return score

# idea from https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
# and from https://github.com/SrinidhiRaghavan/AI-2048-Puzzle/blob/master/Helper.py
# WEIGHT_MATRIX = [[2048, 1024, 64, 32],[512, 128, 16, 2],[256, 8, 2, 1],[4, 2, 1, 1]] for 2048 specifically
def getMatrix(rows, cols):
    # create a gradiantMatrix based on the current row and cols of the board, so the diagonal is not always all 0!
    gradientMatrix = [ [0]*cols for row in range(rows) ]
    for row in range(rows):
        for col in range(cols):
            if row == 0:
                gradientMatrix[row][col] = cols - col - row #first row, last weight is 0
            else:
                gradientMatrix[row][col] = 0 - col - row # minimize weights of middle rows
    return gradientMatrix

def gradient(board):
    score = 0
    rows = len(board)
    cols = len(board[0])
    # recrate gradiantMatrix based on the current row and cols of the board, so the diagonal is not always all 0!
    gradientMatrix = getMatrix(rows, cols)
    # now compute the score
    for row in range(rows):
        for col in range(cols):
            curNum = board[row][col]
            if curNum != 0:
                score += math.log(curNum,10)*gradientMatrix[row][col] # use log of the tile num so the score is not crazy large
    return score

# Weight Matrix Theories from: https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/
# and from http://www.randalolson.com/2015/04/27/artificial-intelligence-has-crushed-all-human-records-in-2048-heres-how-the-ai-pulled-it-off/
# and extremely helpful from https://github.com/Kulbear/endless-2048/blob/master/agent/minimax_agent.py
def evaluation(board):
    # input variables from evaluation functions, so our x1,x2,x3, etc.
    xL = highestNumLocation(board)
    xES = emptySquares(board)
    xMono = monotinicity(board)
    xSmooth = smoothness(board)
    xGrad = gradient(board)
    #print(xL, xES, xMono, xSmooth, xGrad)

    wLocation = 100
    wEmptySquare = 10
    wMono = 1
    wSmooth = 1
    wGrad = 1

    bias1 = 0
    bias2 = 0
    bias3 = 0
    bias4 = 0
    bias5 = 0
    # be careful with the signs here
    return wLocation*(xL + bias1) + wEmptySquare*(xES + bias2) + \
            wMono*(xMono + bias3) + wSmooth*(xSmooth + bias4) + wGrad*(xGrad + bias5)

class RL(object):
    def __init__(self, board, rows, cols):
        self.board = board
        self.rows = rows
        self.cols = cols

    gradientMatrix = [ [4-col-row if row == 0 else 0 for col in range(4)] for row in range(4)]

    def updateMatrix(self):
        for row in range(4):
            for col in range(4):
                curNum = self.board[row][col]
                RL.gradientMatrix[row][col] -= 0.1 #penalize every move used
                if curNum != 0:
                    RL.gradientMatrix[row][col] += 0.1*math.log(curNum,10) #learning rate = 0.1
        #print(RL.gradientMatrix)
    
    def initializeRL():
        RL.gradientMatrix = [ [4-col-row if row == 0 else 0 for col in range(4)] for row in range(4)]

    def evalRL(self):
        # because the gradient matrix is aliased, it will learn as it goes  
        xL = highestNumLocation(self.board)
        xES = emptySquares(self.board)
        xMono = monotinicity(self.board)
        xSmooth = smoothness(self.board)

        xGrad = 0
        # now compute the score
        for row in range(4):
            for col in range(4):
                curNum = self.board[row][col]
                if curNum != 0:
                    xGrad += math.log(curNum,10)*RL.gradientMatrix[row][col] # use log of the tile num so the score is not crazy large

        wLocation = 100
        wEmptySquare = 10
        wMono = 1
        wSmooth = 1
        wGrad = 1

        bias1 = 0
        bias2 = 0
        bias3 = 0
        bias4 = 0
        bias5 = 0
        # be careful with the signs here
        return wLocation*(xL + bias1) + wEmptySquare*(xES + bias2) + \
                wMono*(xMono + bias3) + wSmooth*(xSmooth + bias4) + wGrad*(xGrad + bias5)

##########################################################################################################
# Expectimax AI
##########################################################################################################
def expectimax(board, rows, cols, baseNum, depth, maxDepth, alpha1=-np.inf, alpha2=-np.inf, alpha3=-np.inf, alpha4=-np.inf):
    # use a real-time update board deep copy of the actual board: aiBoard
    if depth == 0:
        return evaluation(board)
    else:
        for treeBranch in range(4):
            #copy a new board and place one random digit onto it
            newBoard = copy.deepcopy(board)
            if treeBranch == 0:
                moveUp(newBoard, rows, cols, baseNum)
                possibleTiles = getAllPossibleTiles(newBoard, rows, cols)
                if possibleTiles != None:
                    for tile in possibleTiles:
                        randomBoard = copy.deepcopy(newBoard)
                        row, col = tile
                        randomBoard[row][col] = baseNum
                        value1 = expectimax(newBoard, rows, cols, baseNum, depth-1, maxDepth, alpha1, alpha2, alpha3, alpha4)
                        alpha1 = max(alpha1, value1)
            elif treeBranch == 1:
                moveLeft(newBoard, rows, cols, baseNum)
                possibleTiles = getAllPossibleTiles(newBoard, rows, cols)
                if possibleTiles != None:
                    for tile in possibleTiles:
                        randomBoard = copy.deepcopy(newBoard)
                        row, col = tile
                        randomBoard[row][col] = baseNum
                        value2 = expectimax(randomBoard, rows, cols, baseNum, depth-1, maxDepth, alpha1, alpha2, alpha3, alpha4)
                        alpha2 = max(alpha2, value2)
            elif treeBranch == 2:
                moveRight(newBoard, rows, cols, baseNum)
                possibleTiles = getAllPossibleTiles(newBoard, rows, cols)
                if possibleTiles != None:
                    for tile in possibleTiles:
                        randomBoard = copy.deepcopy(newBoard)
                        row, col = tile
                        randomBoard[row][col] = baseNum
                        value3 = expectimax(randomBoard, rows, cols, baseNum, depth-1, maxDepth, alpha1, alpha2, alpha3, alpha4)
                        alpha3 = max(alpha3, value3)
            elif treeBranch == 3:
                moveDown(newBoard, rows, cols, baseNum)
                possibleTiles = getAllPossibleTiles(newBoard, rows, cols)
                if possibleTiles != None:
                    for tile in possibleTiles:
                        randomBoard = copy.deepcopy(newBoard)
                        row, col = tile
                        randomBoard[row][col] = baseNum
                        value4 = expectimax(randomBoard, rows, cols, baseNum, depth-1, maxDepth, alpha1, alpha2, alpha3, alpha4)
                        alpha4 = max(alpha4, value4)
        # update alpha to the largest value from 4 moves
        maxValue = max(alpha1, alpha2, alpha3, alpha4)
        if depth == maxDepth:
            # this if statement will run only at top level when recursion goes all the way back
            # not using a dict, using a list to try in order, up first
            dict = [ [alpha1, "Up"],
                    [alpha2, "Left"],
                    [alpha3, "Right"],
                    [alpha4, "Down"]
                    ]
            for i in dict:
                if i[0] == maxValue:
                    return maxValue, i[1]
        return maxValue

#print(expectimax(board))

##########################################################################################################
# Minimax AI
# somehow very similar approach from https://github.com/Kulbear/endless-2048
# more complicated from https://github.com/SrinidhiRaghavan/AI-2048-Puzzle
##########################################################################################################
def getAllPossibleTiles(board, rows, cols):
    possibleChoices = []
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                possibleChoices += [(row, col)]
    #if cannot add a number to the board, just break so as to avoid "empty sequence" error
    if possibleChoices == []:
        return None
    return possibleChoices

def minimax(board, rows, cols, baseNum, depth, maxDepth, isRL, isMax=True, alpha=-np.inf, beta=np.inf):
    # alpha is max score for maxie, beta is min score for mini
    if isRL and depth == maxDepth:
            RL(board,rows,cols).updateMatrix() #update matrix for RL only at the beginning of every move, not for every calculation for a move

    if depth == 0:
        # evaluate when the last step is maxie/player and last depth is <= 1
        if isRL:
            return RL(board, rows, cols).evalRL()
        else:
            return evaluation(board)
    else:
        if isMax:
            #player's turn, 4 moves
            for treeBranch in range(4):
                maxieBoard = copy.deepcopy(board)
                if treeBranch == 0:
                    moveUp(maxieBoard, rows, cols, baseNum)
                    value1 = minimax(maxieBoard, rows, cols, baseNum, depth-1, maxDepth, isRL, False, alpha, beta)
                    alpha = max(alpha, value1)
                    if beta <= alpha:
                        break
                elif treeBranch == 1:
                    moveLeft(maxieBoard, rows, cols, baseNum)
                    value2 = minimax(maxieBoard, rows, cols, baseNum, depth-1, maxDepth, isRL, False, alpha, beta)
                    alpha = max(alpha, value2)
                    if beta <= alpha:
                        break
                elif treeBranch == 2:
                    moveRight(maxieBoard, rows, cols, baseNum)
                    value3 = minimax(maxieBoard, rows, cols, baseNum, depth-1, maxDepth, isRL, False, alpha, beta)
                    alpha = max(alpha, value3)
                    if beta <= alpha:
                        break
                elif treeBranch == 3:
                    moveDown(maxieBoard, rows, cols, baseNum)
                    value4 = minimax(maxieBoard, rows, cols, baseNum, depth-1, maxDepth, isRL, False, alpha, beta)
                    alpha = max(alpha, value4)
                    if beta <= alpha:
                        break
            if depth == maxDepth:
                dict = [ [value1, "Up"],
                        [value2, "Left"],
                        [value3, "Right"],
                        [value4, "Down"]
                        ]
                for i in dict:
                    if i[0] == alpha:
                        return alpha, i[1]
            # still do this for depth > 2 to prevent returning None for even nodes > 2
            return alpha
        else:
            #random generator's turn / min's turn, n possible moves < rows*cols
            possibleTiles = getAllPossibleTiles(board, rows, cols)
            if possibleTiles != None:
                for tile in possibleTiles:
                    miniBoard = copy.deepcopy(board)
                    row, col = tile
                    miniBoard[row][col] = baseNum
                    minValue = minimax(miniBoard, rows, cols, baseNum, depth-1, maxDepth, isRL, True, alpha, beta)
                    beta = min(beta, minValue)
                    if beta <= alpha:
                        break
                return beta
            else:
                return -np.inf
