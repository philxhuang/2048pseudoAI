
#=============================================================================
# Navigation Bar / Top Bar Content
# some additional ideas from # learned from https://pythonprogramming.net/tkinter-menu-bar-tutorial/
# and from https://effbot.org/tkinterbook/tkinter-index.htm
#=============================================================================

# import modules
import random, string, copy, math, os, sys, csv
import numpy as np
from tkinter import *
from tkinter import ttk

rulesText = """Wikipedia's Description:
    2048 is played on a gray 4×4 grid, with numbered tiles that slide smoothly when a player moves them using the four arrow keys.
    Every turn, a new tile will randomly appear in an empty spot on the board with a value of either 2 or 4.
    Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid.
    If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.
    The resulting tile cannot merge with another tile again in the same move. Higher-scoring tiles emit a soft glow.
    Basically, press direction keys on you laptop to merge tiles of the same number!

    Commands:
        Press the respective AIs to toggle activation!
        Up/Down/Left/Right: change the board accordingly
        space: reset board (not loading new parameters)
        c: initialize board (also load new parameters)
        x: recursion depth + 1
        z: recursion depth - 1
        e: toggle Evil Mode
        a: toggle Auto Run Mode (reset board when game is over--->mostly for RL AI)

        r: Record the current board status with the type of algorithm that is working (please do so only when game is over so we have good data!)
        i: Statistics for Expectimax Performance
        o: Statistics for Minimax Performance
        p: Statistics for Reinforcement Learning Performance
    """
parametersText = """
    Here are the parameters you can customize in this game without modifying the source code:

    Number of Rows [Default=4] (4 <= integer <= 10)
    
    Number of Columns [Default=4] (4 <= integer < 10)
    
    Base Number [Default=2] (2 <= integer <= 10)
        ---> The lowest non-0 number to begin with; the second largest number will be base number squared
        ---> cannot be 1 because 1**2 = 1
    
    Base Probability [Default=90] (0 <= integer <= 100)
        ---> The probability that the base number will be randomly generated
        ---> accordingly, the square number will have the probability of (100-baseProb)%
    """
expectimaxText = """
    Expectimax AI Algorithm:

    The expectimax algorithm is the simplest of the three AIs to understand.
    It basically simulates all four possible player moves first (Up/Down/Left/Right), 
    and for each player move, it branches into many moves based on how many empty tiles exist.
    Then the computer will generate a random tile on an empty tile, and the player will choose a move, so on so forth.

    When Expectimax reaches the max depth, it will return the best score upwards, eventually deciding the best move on the top level.
    Because any move/node can create the max score, Expectimax must evaluate all boards, therefore being slow.
    """

minimaxText = """
    Minimax AI Algorithm with Alpha-Beta Pruning:

    The minimax algorithm (a.k.a MinMax, MM or saddle point) will simulate two players against each other.
    The first player (maxie) makes a move (Up/Down/Left/Right) and the score of that board is evaluated.
        ---> creating 4 nodes
    For each of the four moves, the random # generator (mini) will generate a number on an empty tile, and every possible randomly generated board is again evaluated.
        ---> creating n nodes (n = all empty tiles of the previous board)
    When Minimax reaches the max depth, it will return the best score upwards, eventually deciding the best move on the top level.

    Alpha-Beta Pruning allows the Minimax Algorithm to keep track of the max & min score every recorded,
    so that the algorithm can eliminate brances that it knows it never needs to evaluate, thus improving efficiency.
    For more detailed descriptions, please check out the Github page.
    """

RLText = """
    Reinforcement Learning (RL) Algorithm:

    Reinforcement Learning, or Q-Learning, is using the same recursion model as minimax.
    The difference is how every board is scored.
    The weight/gradient matrix, which is one of the functions to determine the score of every node/board/move, is coded as an object attribute.
    Because this "global" object attribute allows aliasing, it will be changed every time it is called after every move, thus self-learning.

    The initial matrix has only a general guideline. As moves made increase, the matrix will evolve to get closer to the best evaluation scheme.
    For example:    [ [3,2,1,0],                        [ [154, 112, 74, 32],
                      [0,0,0,0],    may evolve into       [34, 24, 14, 5],
                      [0,0,0,0],                          [7, 3, -1, -4],
                      [0,0,0,0] ]                         [-2, -12, -26, -52] ]
    """

designText = """
    Game Design:

    This game is designed in Python in the follow structure:
    1. The __init__.py file contains the board as an object. It also has tkinter canvas codes for drawing the board and other game commands
    2. The navigation.py file contains documentations, top bar content, and a fractal used to demonstrate the AI algorithms.
    3. The ai.py file contains all 3 AI algorithms. Expectimax and Minimax are made by modifying a deep copy of the board from __init__.py,
        and then find the best move so as to avoid aliasing problems. The Reinforcement Learning is made similarly to minimax, but the evaluaion
        scheme is coded in an object. The class attribute allows the weight/gradient matrix to learn/accumulate without being erased every time on call.
    4. The dataVisualization.py uses matplotlib to pull data from pre-loaded CSV files in order to visualize the performances of algorithms.

    The Evaluation Scheme cannot be changed by simply playing the game. Experienced programmer can download the source code and change internally.
    Here is how the evaluation function works:
    def evaluation(board):

    xL = highestNumLocation(board) #keep the highest score tile at top left
    xES = emptySquares(board) # bonus for more empty tiles ---> encourage merging
    xMono = monotinicity(board) # bonus for making rows/cols either strictly decreasing from the left cornor
    xSmooth = smoothness(board) # measures the difference between neighboring tiles and tries to minimize this count; used log10
    xGrad = gradient(board) # create a gradiantMatrix based on the current row and cols of the board to evaluate the board, used log10

    # These weights are standardized. Feel free to change them or make them learn!
    wLocation = 100
    wEmptySquare = 10
    wMono = 1
    wSmooth = 1
    wGrad = 2

    bias1 = 0
    bias2 = 0
    bias3 = 0
    bias4 = 0
    bias5 = 0

    return wLocation*(xL + bias1) + wEmptySquare*(xES + bias2) + 
            wMono*(xMono + bias3) + wSmooth*(xSmooth + bias4) + wGrad*(xGrad + bias5)
    """

def rules(windowWidth=600, windowHeight=500):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    canvas.create_text(windowWidth//2, windowHeight//2, text=rulesText, width=windowWidth-10)

def parameters(windowWidth=500, windowHeight=300):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    canvas.create_text(windowWidth//2, windowHeight//2, text=parametersText, width=windowWidth-10)

def design(windowWidth=800, windowHeight=600):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=windowWidth, height=windowHeight, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    canvas.create_text(windowWidth//2, windowHeight//2, text=designText, width=windowWidth-10)
#==========================================================================================
# AI Component winows has a totally different canvas to show selection & fractals
# sourced from Carnegie Mellon University 15-112 Spring 2019 page
# =========================================================================================
def init(data):
    data.minimax = False
    data.expectimax = False
    data.RL = False
    data.depth = 0

def mousePressed(event, data):
    if 10 <= event.y <= 30:
        if data.width//8 <= event.x <= data.width*3//8-10:
            data.expectimax = not data.expectimax
            data.minimax = False
            data.RL = False
        elif data.width*3//8 <= event.x <= data.width*5//8-10:
            data.expectimax = False
            data.minimax = not data.minimax
            data.RL = False
        elif data.width*5//8 <= event.x <= data.width*7//8:
            data.expectimax = False
            data.minimax = False
            data.RL = not data.RL
    if 30 <= event.x <= 150:
        if data.height//2 <= event.y <= data.height//2+40:
            if data.depth < 6:
                data.depth += 1
        elif data.height//2+50 <= event.y <= data.height//2+90:
            if data.depth > 0:
                data.depth -= 1

def drawFractals(canvas, startX, startY, depth, prevX, prevY, isMaxie=True, heightGap=40):
    # the gaps are actually half of the gap!
    if depth == 0:
        canvas.create_line(startX, startY-5, prevX, prevY)
        canvas.create_oval(startX-5,startY-5,startX+5,startY+5, fill="green" if isMaxie else None)
    elif isMaxie:
        drawFractals(canvas, startX-60*2, startY+heightGap, 0, startX, startY, isMaxie=True)
        drawFractals(canvas, startX-60, startY+heightGap, 0, startX, startY, isMaxie=True)
        drawFractals(canvas, startX+60, startY+heightGap, 0, startX, startY, isMaxie=True)
        drawFractals(canvas, startX+60*2, startY+heightGap, 0, startX, startY, isMaxie=True)

        drawFractals(canvas, startX-60*2, startY+heightGap, depth-1, startX, startY, isMaxie=False)
        drawFractals(canvas, startX-60, startY+heightGap, depth-1, startX, startY, isMaxie=False)
        drawFractals(canvas, startX+60, startY+heightGap, depth-1, startX, startY, isMaxie=False)
        drawFractals(canvas, startX+60*2, startY+heightGap, depth-1, startX, startY, isMaxie=False)
    else:
        drawFractals(canvas, startX-80, startY+heightGap, 0, startX, startY, isMaxie=False)
        drawFractals(canvas, startX+80, startY+heightGap, 0, startX, startY, isMaxie=False)

        drawFractals(canvas, startX-80, startY+heightGap, depth-1, startX, startY, isMaxie=True)
        drawFractals(canvas, startX+80, startY+heightGap, depth-1, startX, startY, isMaxie=True)

def redrawAll(canvas, data):
    canvas.create_rectangle(data.width//8, 10, data.width*3//8-10, 30, fill="pink" if data.expectimax else "#8f7a66")
    canvas.create_text(data.width//4, 20, text="Expectimax AI")

    canvas.create_rectangle(data.width*3//8, 10, data.width*5//8-10, 30, fill="pink" if data.minimax else "#8f7a66")
    canvas.create_text(data.width*2//4, 20, text="Minimax AI")

    canvas.create_rectangle(data.width*5//8, 10, data.width*7/8, 30, fill="pink" if data.RL else "#8f7a66")
    canvas.create_text(data.width*3//4, 20, text="Reinforcement Learning AI")

    if data.expectimax:
        canvas.create_text(data.width//2, data.height//4, text=expectimaxText, width=data.width-10)
    elif data.minimax:
        canvas.create_text(data.width//2, data.height//4, text=minimaxText, width=data.width-10)
    elif data.RL:
        canvas.create_text(data.width//2, data.height//4, text=RLText, width=data.width-10)
    
    canvas.create_rectangle(30, data.height//2, 150, data.height//2+40, fill="pink")
    canvas.create_text(90, data.height//2+20, text="Increase")

    canvas.create_rectangle(30, data.height//2+50, 150, data.height//2+90, fill="pink")
    canvas.create_text(90, data.height//2+70, text="Decrease")

    canvas.create_oval(80, data.height//2+110, 100, data.height//2+130, fill="green")
    canvas.create_text(90, data.height//2+100, text="Mini Node")
    canvas.create_text(90, data.height//2+180, text="Note: This tree only shows two nodes/possible tiles for every player's move for the same of clarity.", width=150)

    canvas.create_text(data.width//2-60,data.height//2-10, text="Current Depth")
    canvas.create_text(data.width//2-60,data.height//2+10, text=str(data.depth))

    canvas.create_oval(data.width//2-15,data.height//2-15,data.width//2+15,data.height//2+15)
    drawFractals(canvas, data.width//2, data.height//2, data.depth, data.width//2, data.height//2)

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='#bbada0', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    init(data)

    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=width, height=height, background="#bbada0")
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    canvas.create_rectangle(data.width//8, 10, data.width*3//8-10, 30, fill="#8f7a66")
    canvas.create_text(data.width//4, 20, text="Expectimax AI")

    canvas.create_rectangle(data.width*3//8, 10, data.width*5//8-10, 30, fill="#8f7a66")
    canvas.create_text(data.width*2//4, 20, text="Minimax AI")

    canvas.create_rectangle(data.width*5//8, 10, data.width*7/8, 30, fill="#8f7a66")
    canvas.create_text(data.width*3//4, 20, text="Reinforcement Learning AI")
    
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed

def AIComponents(windowWidth=1200, windowHeight=550):
    run(windowWidth,windowHeight)

#==========================================================================================
# Topbar ---> Top level functions
# adapted and modified from https://effbot.org/tkinterbook/menu.htm
# =========================================================================================
def topBar(root):
    # create top bar before the canvas
    menuBar = Menu(root)
    menuBar.add_command(label="Exit", command=root.quit)
        
    # create a pulldown menu, and add it to the menu bar
    menuBar.add_command(label="Game Rules & Commands", command=rules)
    menuBar.add_command(label="Customize Parameters", command=parameters)
    menuBar.add_command(label="AI Components", command=AIComponents)
    menuBar.add_command(label="Design (Source Code)", command=design)

    # display the menu
    root.config(menu=menuBar)

#==========================================================================================
# Customization & Validation of Inputs
# mostly learned from https://effbot.org/tkinterbook/tkinter-index.htm
# =========================================================================================
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
        if rows.isdigit() and 4 <= int(rows) <= 10:
            data.rows = int(rows)
        
        cols = colsInput.get()
        if cols.isdigit() and 4 <= int(cols) <= 10:
            data.cols = int(cols)

        baseNum = baseNumInput.get()
        if baseNum.isdigit() and 2 <= int(baseNum) <= 10:
            data.baseNum = int(baseNum)
        
        baseProb = baseProbInput.get()
        if baseProb.isdigit() and 0 <= int(baseProb) <= 100:
            data.baseProb = int(baseProb)
    
    setButton = Button(root, text="Load New Parameters", command=getParas)
    setButton.pack()
    setButton.place(x=data.width-data.rightMargin*0.4,y=data.height//2+140)
