
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
    menuBar.add_command(label="Game Rules & Commands", command=rules)
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
    rowsInput = Entry(root)
    rowsInput.pack()
    rowsInput.place(x=data.width-data.rightMargin//2,y=data.topMargin,width=data.rightMargin//2.5)

    colsInput = Entry(root)
    colsInput.pack()
    colsInput.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height//8,width=data.rightMargin//2.5)

    baseNumInput = Entry(root)
    baseNumInput.pack()
    baseNumInput.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height*2//8, width=data.rightMargin//2.5)

    baseProbInput = Entry(root)
    baseProbInput.pack()
    baseProbInput.place(x=data.width-data.rightMargin//2,y=data.topMargin+data.height*3//8,width=data.rightMargin//2.5)

    def getParas():
        # get inputs and validate; inputs are strings
        rows = rowsInput.get()
        if rows.isdigit() and 3 < int(rows) <= 10:
            data.rows = int(rows)
        
        cols = colsInput.get()
        if cols.isdigit() and 3 < int(cols) <= 10:
            data.cols = int(cols)

        baseNum = baseNumInput.get()
        if baseNum.isdigit() and 1 < int(baseNum) <= 10:
            data.baseNum = int(baseNum)
        
        baseProb = baseProbInput.get()
        if baseProb.isdigit() and 0 <= int(baseProb) <= 100:
            data.baseProb = int(baseProb)
    
    setButton = Button(root, text="Load New Parameters", command=getParas)
    setButton.pack()
    setButton.place(x=data.width-data.rightMargin*0.5,y=data.height-data.topMargin*2.2)
