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
#=============================================================================


# Animation code and OOPy animation organization adapted from:
# https://www.youtube.com/watch?v=27hjc9sU-Z0
import random, string
import numpy, torch
from tkinter import *
from ttk import Button, Combobox


class maxtrix(object):

    # Model
    def __init__(self, rows, cols):
        pass

    # View
    def draw(self, canvas):
        pass

    # Controller
    def move(self, data):
        pass

# Core animation code

def init(data):
    pass

def mousePressed(event, data):
    pass

def redrawAll(canvas, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    pass


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
