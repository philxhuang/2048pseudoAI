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
from ai import expectiMax
from ai import isGameOver

class matrix(object):
#=======================================================Model================================================
    def __init__(self, rows, cols, width, height, margin, fill):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.margin = margin
        self.fill = fill
        #boxWidth, boxHeight will be scaled to data.width, data.height by tkinter run() at the very end
        self.boxWidth = self.width // self.cols
        self.boxHeight = self.height // self.rows
        self.board = [ [self.fill]*self.cols for row in range(self.rows) ]
        #deep copy the same board for AI so we do not mess up
        self.aiBoard = copy.deepcopy(self.board)
    
    def initializeBoard(self):
        #use list comprehension to reset the board, here is a 2d list of 0
        self.board = [ [self.fill]*self.cols for row in range(self.rows) ]
    
    def getItem(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
    
    def getColor(self, item):
        #color sourced from https://flatuicolors.com/palette/defo
        self.colors = {0:"#f1c40f", #0 will never print! a place holder color/basecolor for the board, or use "#eee4da"
                       2: "#f39c12",
                       4: "#e67e22",
                       8: "#d35400",
                       16: "#e74c3c",
                       32: "#c0392b",
                       64: "#1abc9c",
                       128: "#16a085",
                       256: "#2ecc71",
                       512: "#27ae60", #2^10 power!
                       1024: "#3498db",
                       2048: "#2980b9",
                       4096: "#9b59b6",
                       8192: "#8e44ad",
                       16384: "#34495e", #starting black here to whiter grey below
                       32768: "#2c3e50",
                       65536: "##7f8c8d",
                       131072: "#95a5a6",
                       262144: "#bdc3c7",
                       524288: "#ecf0f1" #"clouds color", almost impossible to achieve to my knowledge, challenge me! :)
                        }
        return self.colors[item]

    # Controller
    def generateRandomNumber(self):
        numberChoices = [2,4]
        #this is a cheating way to creating random num with different %
        getPercentage = random.randint(1, 100) #randint is inclusive on both sides!
        if getPercentage <= 10: #out of 100, so 90% num is 2, 10%num is 4
            return numberChoices[1] #which is 4
        else:
            return numberChoices[0] #which is 2

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
                    self.board[row][col] *= 2
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
                    self.board[row][col] *= 2
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
                    self.board[row][col] *= 2
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
                    self.board[row][col] *= 2
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

#==================================================View===============================================
    def draw(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                num = self.getItem(row, col)
                color = self.getColor(num)
                # SUPER IMPORTANT: width=cols, height=rows!
                canvas.create_rectangle(col*self.boxWidth+self.margin, row*self.boxHeight+self.margin, 
                                        (col+1)*self.boxHeight-self.margin, (row+1)*self.boxWidth-self.margin,
                                        fill=color, outline="")
                #draw box first, then put numbers on top. Text is scalled to the dimensions too! How nice!
                canvas.create_text((col+0.5)*self.boxWidth, (row+0.5)*self.boxHeight, text=str(num),
                                    font="Arial "+str((self.boxHeight+self.boxHeight)//6))

#=================================================================================================
# Core animation code
# sourced from Carnegie Mellon University 15-112 Spring 2019 page
#==================================================================================================
#View
def init(data):
    data.rows = 4
    data.cols = 4
    data.fill = 0
    data.margin = 10
    data.board = matrix(data.rows, data.cols, data.width, data.height,
                        data.margin, data.fill)
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
        data.board.placeRandomNumber()
    elif event.keysym == "Right":
        data.board.moveRight()
        data.board.placeRandomNumber()
    elif event.keysym == "Up":
        data.board.moveUp()
        data.board.placeRandomNumber()
    elif event.keysym == "Down":
        data.board.moveDown()
        data.board.placeRandomNumber()
    elif event.keysym == "space":
        #remake the empty board and put two numbers back in
        data.board.initializeBoard()
        data.board.placeRandomNumber()
        data.board.placeRandomNumber()

def timerFired(data):
    data.timerDelay = 50 #1000ms = 1s
    if not isGameOver(data.board.board):
        #changing the defineDepth here ---> also change the maxDepth in ai.py
        getAIMoves(data, 2)

def getAIMoves(data, definedDepth):
    #avoid aliasing the board that would cause massive problem
    board = data.board.board
    bestMove = expectiMax(board, data.rows, data.cols, definedDepth)[1]
    if not isinstance(bestMove, str): return
    if bestMove == "Left":
        data.board.moveLeft()
        data.board.placeRandomNumber()
    elif bestMove == "Right":
        data.board.moveRight()
        data.board.placeRandomNumber()
    elif bestMove == "Up":
        data.board.moveUp()
        data.board.placeRandomNumber()
    elif bestMove == "Down":
        data.board.moveDown()
        data.board.placeRandomNumber()
    data.board.board = board

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

run(600, 600)
