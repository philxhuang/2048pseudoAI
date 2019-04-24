#=============================================================================
# 15-112 Term Project Spring 2019
# Phil Huang
# ID: xiangheh
# Recitation Section: G
#=============================================================================
# This TP is largely inspired by the 2048 AI from two JavaScript sources:
# https://github.com/ovolve/2048-AI and https://github.com/ronzil/2048-AI
# Algorithm consideration from StackOverflow post:
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#
# PyTorch learned from Udacity AI courses for free
# Some animation code and OOPy animation organization adapted from:
# https://www.youtube.com/watch?v=27hjc9sU-Z0
#=============================================================================

# import modules
import random, string, copy, math, os, sys
import numpy as np
import pandas as pd
import torch
from tkinter import *
from tkinter import ttk
# import other files
from ai import expectimax
from ai import minimax
from ai import isGameOver
# import matplotlib if usable
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class matrix(object):
#=======================================================Model================================================
    def __init__(self, rows, cols, width, height, tileMargin, boardMargin, topMargin, rightMargin, baseNum, baseProb, fill):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

        self.tileMargin = tileMargin
        self.topMargin = topMargin
        self.rightMargin = rightMargin
        self.boardMargin = boardMargin

        self.boardWidth = self.width - self.rightMargin
        self.boardHeight = self.height - self.topMargin
        #boxWidth, boxHeight will be scaled to data.width, data.height by tkinter run() at the very end
        self.boxWidth = self.boardWidth // self.cols
        self.boxHeight = self.boardHeight // self.rows

        self.baseNum = baseNum
        self.baseProb = baseProb
        self.fill = fill
        self.board = [ [self.fill]*self.cols for row in range(self.rows) ]
    
    def initializeBoard(self):
        #use list comprehension to reset the board, here is a 2d list of 0
        self.board = [ [self.fill]*self.cols for row in range(self.rows) ]
    
    def getItem(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
    
    def getColor(self, item):
        #color sourced from https://flatuicolors.com/palette/defo
        self.colors = {self.fill:"#f1c40f", #0 will never print! a place holder color/basecolor for the board, or use "#eee4da"
                       self.baseNum: "#f39c12",
                       self.baseNum**2: "#e67e22",
                       self.baseNum**3: "#d35400",
                       self.baseNum**4: "#e74c3c",
                       self.baseNum**5: "#c0392b",
                       self.baseNum**6: "#1abc9c",
                       self.baseNum**7: "#16a085",
                       self.baseNum**8: "#2ecc71",
                       self.baseNum**9: "#27ae60",
                       self.baseNum**10: "#3498db", # baseNum^10 power!
                       self.baseNum**11: "#2980b9",
                       self.baseNum**12: "#9b59b6",
                       self.baseNum**13: "#8e44ad",
                       self.baseNum**14: "#34495e", #starting black here to whiter grey below
                       self.baseNum**15: "#2c3e50",
                       self.baseNum**16: "##7f8c8d",
                       self.baseNum**17: "#95a5a6",
                       self.baseNum**18: "#bdc3c7",
                       self.baseNum**19: "#ecf0f1" #"clouds color", almost impossible to achieve to my knowledge, challenge me! :)
                        }
        return self.colors[item]

    # Controller
    def generateRandomNumber(self):
        numberChoices = [self.baseNum, self.baseNum**2]
        #this is a cheating way to creating random num with different %
        getPercentage = random.randint(1, 100) #randint is inclusive on both sides!
        if getPercentage <= self.baseProb: #out of 100, so 90% num is 2, 10% num is 4
            return numberChoices[0] #which is 2
        else:
            return numberChoices[1] #which is 4

    def placeRandomNumber(self):
        newNum = self.generateRandomNumber()
        possibleChoices = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == self.fill: #meaning empty box
                    possibleChoices += [(row, col)]
        #if cannot add a number to the board, just break so as to avoid "empty sequence" error
        if possibleChoices == []:
            return
        finalRow, finalCol = random.choice(possibleChoices)
        self.board[finalRow][finalCol] = newNum

#====================================4 move left+right algorithms=====================================
    def moveLeft(self):
        #only for mergeing
        for row in range(self.rows):
            for col in range(self.cols-1): #avoid "out of index" error, 1,2,3
                self.shiftLeft(row)
                curNum = self.board[row][col]
                nextNum = self.board[row][col+1]
                if curNum == nextNum:
                    self.board[row][col] *= self.baseNum
                    self.board[row][col+1] = self.fill
            self.shiftLeft(row)

    def shiftLeft(self, row):
        # shift after merging everything in a row, AVOID DESTRUCTIVELY MODIFYING THE LIST!
        # otherwise would skip 0s, so [2,0,0,2] would not work
        curRow = self.board[row]
        shiftCount = curRow.count(self.fill) #only do it as many times as how many 0's are in this row
        index = 0
        count = 0
        while index < len(curRow) and count < shiftCount:
            if curRow[index] == self.fill:
                 curRow.pop(index)
                 curRow.append(self.fill)
                 count += 1
            else:
                index += 1
    
    def moveRight(self):
        #only for mergeing
        for row in range(self.rows):
            for col in range(self.cols-1, 0, -1): #avoid "out of index" error, so 3,2,1
                self.shiftRight(row)
                curNum = self.board[row][col]
                nextNum = self.board[row][col-1]
                if curNum == nextNum:
                    self.board[row][col] *= self.baseNum
                    self.board[row][col-1] = self.fill
            self.shiftRight(row)

    def shiftRight(self, row):
        curRow = self.board[row]
        shiftCount = curRow.count(self.fill)
        index = -1
        count = 0
        while index > -len(curRow): # -1,-2,-3
            if curRow[index] == self.fill and count < shiftCount:
                 curRow.pop(index)
                 curRow.insert(0, self.fill) # replace with a 0 at the beginning/left
                 count += 1
            else:
                index -= 1
#====================================4 move up+down algorithms=====================================
    def moveUp(self):
        #only for mergeing
        for col in range(self.cols):
            for row in range(self.rows-1):
                self.shiftUp(col)
                curNum = self.board[row][col]
                nextNum = self.board[row+1][col]
                if curNum == nextNum:
                    self.board[row][col] *= self.baseNum
                    self.board[row+1][col] = self.fill
            self.shiftUp(col)
    
    def shiftUp(self, col):
        curCol = []
        for row in range(self.rows): # IMPORTANT note: need to transform cols to a row
            curCol += [ self.board[row][col] ]
        shiftCount = curCol.count(self.fill) #only do it as many times as how many 0's are in this row
        index = 0
        count = 0
        while index < len(curCol) and count < shiftCount:
            if curCol[index] == self.fill:
                 curCol.pop(index)
                 curCol.append(self.fill)
                 count += 1
            else:
                index += 1
        for row in range(self.rows): #now slap the new list of col #s back to the board
            self.board[row][col] = curCol[row]

    def moveDown(self):
        for col in range(self.cols):
            for row in range(self.rows-1, 0, -1): #3,2,1 not including 0
                self.shiftDown(col)
                curNum = self.board[row][col]
                nextNum = self.board[row-1][col]
                if curNum == nextNum:
                    self.board[row][col] *= self.baseNum
                    self.board[row-1][col] = self.fill
            self.shiftDown(col)

    def shiftDown(self, col):
        curCol = []
        for row in range(self.rows):
            curCol += [ self.board[row][col] ]
        shiftCount = curCol.count(self.fill) #only do it as many times as how many 0's are in this row
        index = -1
        count = 0
        while index > -len(curCol) and count < shiftCount: #-1,-2,-3
            if curCol[index] == self.fill:
                 curCol.pop(index)
                 curCol.insert(0, self.fill)
                 count += 1
            else:
                index -= 1
        for row in range(self.rows): #now slap the new list of col #s back to the board
            self.board[row][col] = curCol[row]

##########################################################################################################
# Evil AI Mode
# inspirations from https://github.com/sztupy/2048-Hard
# and from this Evil 2048 AI here https://github.com/aj-r/Evil-2048
##########################################################################################################
    def findMaxEvil(self, evilMatrix):
        # the lowest maxNum is guaranteed to be 2, which is > -1
        targetRow = 0
        targetCol = 0
        maxNum = -1
        for row in range(self.rows):
            for col in range(self.cols):
                curNum = evilMatrix[row][col]
                if curNum > maxNum:
                    maxNum = curNum
                    targetRow = row
                    targetCol = col
        return maxNum, targetRow, targetCol

    def getEvilMaxtrix(self):
        # use the sum of adjacent tiles to comput the most annoying tile position possible
        probMatrix = [ [0]*self.cols for row in range(self.rows) ]
        for row in range(self.rows):
            for col in range(self.cols):
                curNum = self.board[row][col]
                if curNum != self.fill:
                    for r,c in [(0,1),(1,0),(0,-1),(-1,0)]:
                        # try all four directions, but no wrap-around
                        if self.rows > row+r >= 0 and self.cols > col+c >= 0 \
                            and self.board[row+r][col+c] == self.fill:
                            probMatrix[row+r][col+c] += curNum
        return probMatrix

    def evilAIMove(self):
        # use probability to put a tile in the most annoying place
        evilMatrix = self.getEvilMaxtrix()
        evilNum, evilRow, evilCol = self.findMaxEvil(evilMatrix)
        newNum = self.generateRandomNumber()
        self.board[evilRow][evilCol] = newNum

#==================================================View===============================================
    def draw(self, canvas):
        canvas.create_rectangle(self.boardMargin, self.topMargin + self.tileMargin - self.boardMargin,
                                self.boardWidth - self.boardMargin, self.topMargin + self.boardHeight - self.boardMargin, fill="")
        for row in range(self.rows):
            for col in range(self.cols):
                num = self.getItem(row, col)
                color = self.getColor(num)
                # SUPER IMPORTANT: width=cols, height=rows!
                canvas.create_rectangle(col*self.boxWidth + self.tileMargin + self.boardMargin,
                                        row*self.boxHeight + self.tileMargin + self.topMargin + self.boardMargin, 
                                        (col+1)*self.boxWidth - self.tileMargin - self.boardMargin, 
                                        (row+1)*self.boxHeight - self.tileMargin + self.topMargin - self.boardMargin,
                                        fill=color, outline="")
                #draw box first, then put numbers on top. Text is scalled to the dimensions too! How nice!
                canvas.create_text((col+0.5)*self.boxWidth, (row+0.5)*self.boxHeight + self.topMargin,
                                    text=str(num), font="Arial "+str((self.boxHeight + self.boxWidth)//10))
                #also tell the powers of the tiles based on the self.baseNum
                if num != 0:
                    canvas.create_text((col+0.5)*self.boxWidth, (row+0.75)*self.boxHeight + self.topMargin,
                                        text=str( int(math.log(num,self.baseNum)) )+"th Power", font="Arial "+str((self.boxHeight + self.boxWidth)//20))

#=================================================================================================
# Core animation code
# sourced from Carnegie Mellon University 15-112 Spring 2019 page
#==================================================================================================
#View
def init(data):
    data.rows = 4
    data.cols = 4
    data.fill = 0

    data.tileMargin = 5
    data.boardMargin = 5
    data.topMargin = 100
    data.rightMargin = 250

    data.baseNum = 2
    data.baseProb = 90

    data.board = matrix(data.rows, data.cols, data.width, data.height,
                        data.tileMargin, data.boardMargin, data.topMargin, data.rightMargin,
                        data.baseNum, data.baseProb, data.fill)

    #start with normal mode
    data.isGameOver = False
    data.isAI = True

    data.isEvilMode = False
    data.isExpectimax = False
    data.isMinimax = True
    #initial board has two numbers, so this is not redundant but iterative design

    data.board.placeRandomNumber()
    data.board.placeRandomNumber()

#Controller
def mousePressed(event, data):
    pass

def keyPressed(event, data):
    # use event.keysym here
    if event.keysym == "Left":
        data.board.moveLeft()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif event.keysym == "Right":
        data.board.moveRight()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif event.keysym == "Up":
        data.board.moveUp()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif event.keysym == "Down":
        data.board.moveDown()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif event.keysym == "space":
        #remake the empty board and put two numbers back in
        data.board.initializeBoard()
        data.board.placeRandomNumber()
        data.board.placeRandomNumber()

def timerFired(data):
    data.timerDelay = 50 #1000ms = 1s
    #changing the defineDepth here ---> also change the maxDepth in ai.py
    if data.isAI:
        getAIMove(data, 2, 2)
    #if data.isGameOver or isGameOver(data.board.board, data.baseNum):
        #data.board.initializeBoard()

def getAIMove(data, definedDepth, maxDepth):
    #avoid aliasing the board that would cause massive problem
    board = copy.deepcopy(data.board.board)
    if data.isExpectimax:
        bestScore, bestMove = expectimax(board, data.rows, data.cols, data.baseNum, definedDepth, maxDepth)
    elif data.isMinimax:
        bestScore, bestMove = minimax(board, data.rows, data.cols, data.baseNum, definedDepth, maxDepth)

    if bestScore == -np.inf: data.isGameOver = True

    if bestMove == "Left":
        data.board.moveLeft()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif bestMove == "Right":
        data.board.moveRight()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif bestMove == "Up":
        data.board.moveUp()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()
    elif bestMove == "Down":
        data.board.moveDown()
        if data.isEvilMode:
            data.board.evilAIMove()
        else:
            data.board.placeRandomNumber()

#Model
def redrawAll(canvas, data):
    data.board.draw(canvas)

#=======================================================================================
# use the run function as-is
# sourced from Carnegie Mellon University 15-112 Spring 2019 page
#=======================================================================================

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='#bbada0', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 600)
