
#=============================================================================
# Navigation Bar / Top Bar Content
# some additional ideas from # learned from https://pythonprogramming.net/tkinter-menu-bar-tutorial/
# and from https://effbot.org/tkinterbook/tkinter-index.htm
#=============================================================================

# import modules
import random, string, copy, math, os, sys
import numpy as np
import pandas as pd
import torch
from tkinter import *
from tkinter import ttk
# import other files
from ai import expectimax, minimax, isGameOver
# import matplotlib if usable
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def rules(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()


def parameters(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()


def minimax(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()


def expectimax(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()


def RLAlgo(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()


def design(windowWidth=600, windowHeight=400):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

# adapted and modified from https://effbot.org/tkinterbook/menu.htm
def topBar(root):
    # create top bar before the canvas
    menuBar = Menu(root)
    menuBar.add_command(label="Exit", command=root.quit)
        
    # create a pulldown menu, and add it to the menu bar
    menuBar.add_command(label="Game Rules", command=rules)
    menuBar.add_command(label="Customizable Parameters", command=parameters)

    AIMenu = Menu(menuBar, tearoff=0)
    AIMenu.add_command(label="Minimax", command=minimax)
    AIMenu.add_command(label="Expectimax", command=expectimax)
    AIMenu.add_command(label="RL Algorithm", command=RLAlgo)
    menuBar.add_cascade(label="AI Components", menu=AIMenu)

    menuBar.add_command(label="Design (Source Code)", command=design)

    # display the menu
    root.config(menu=menuBar)

#=============================================================================
# Customization
# ===========================================================================
def customize(root, data):
# all customizable parameters are changed here, including input validations
    rowsLabel = Label(root, text="# of Rows", font=("Arial", 10), background="#8f7a66")
    rowsLabel.pack()
    rowsLabel.place(x=5+data.width-data.rightMargin,y=data.topMargin,width=data.rightMargin//3)
    rowsInput = Entry(root)
    rowsInput.pack()
    rowsInput.place(x=data.width-data.rightMargin//2,y=data.topMargin,width=data.rightMargin//2.5)

    colsLabel = Label(root, text="# of Columns", font=("Arial", 10), background="#8f7a66")
    colsLabel.pack()
    colsLabel.place(x=5+data.width-data.rightMargin,y=data.topMargin+data.height//8,width=data.rightMargin//2.5)
    cols = Entry(root)
    cols.pack()
    cols.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height//8,width=data.rightMargin//2.5)

    baseNum = Label(root, text="The Base Number", font=("Arial", 10), background="#8f7a66")
    baseNum.pack()
    baseNum.place(x=5+data.width-data.rightMargin,y=data.topMargin+data.height*2//8,width=data.rightMargin//2.5)
    baseNum = Entry(root)
    baseNum.pack()
    baseNum.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height*2//8, width=data.rightMargin//2.5)

    baseProb = Label(root, text="Base Probability", font=("Arial", 10), background="#8f7a66")
    baseProb.pack()
    baseProb.place(x=5+data.width-data.rightMargin,y=data.topMargin+data.height*3//8,width=data.rightMargin//2.5)
    baseProb = Entry(root)
    baseProb.pack()
    baseProb.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height*3//8,width=data.rightMargin//2.5)

    def getParas():
        # any input is a string
        rows = rowsInput.get()
        if rows.isdigit() and 0 < int(rows) <= 10:
            data.rows = int(rows)
        data.board.initializeBoard()
        data.board.placeRandomNumber()
        data.board.placeRandomNumber()
    
    setButton = Button(root, text="Start New Board", command=getParas)
    setButton.pack()
    setButton.place(x=data.width-data.rightMargin//2,y=data.height-data.topMargin//2)
