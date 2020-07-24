import random
import sys
import os
from termcolor import colored,cprint
import colorama

colorama.init()
clear = lambda: os.system('cls')

#Ta inn input og set width og height (og antal bomber). Bruk .isdigit() og sjekk at x > 0

width = 20 #int(input('Set width: '))
height = 10
bombNumber = 25

theBoard = []
theHiddenBoard = []
listBombs = []
theHBC = []

def makeBoard(board, w, h):
    x = ['*','-','|']
    for i in range(h+2):
        board.append([])
    for i in range(h+2):
        for j in range(w+2):
            if i == 0 or i == h+1:
                board[i].append(x[1])
            elif j == 0 or j == w+1:
                board[i].append(x[2])
            else:
                board[i].append(x[0])

makeBoard(theHBC, width, height)

def printBoard(board,w,h):
    clear()
    col = theHBC
    for j in range(1,h+1):
        for k in range(1,w+1):
            col[j][k] = colored(board[j][k],'white')
            if col[j][k] != colored('*','white'):
                if col[j][k] == colored('1','white'):
                    col[j][k] = colored(board[j][k],'cyan')
                elif col[j][k] == colored('2','white'):
                    col[j][k] = colored(board[j][k],'green')
                elif col[j][k] == colored('3','white'):
                    col[j][k] = colored(board[j][k],'magenta')
                elif col[j][k] == colored('4','white'):
                    col[j][k] = colored(board[j][k],'blue')
                elif col[j][k] == colored('5','white'):
                    col[j][k] = colored(board[j][k],'brown')
                elif col[j][k] == colored('x', 'white'):
                    col[j][k] = colored(board[j][k], 'red')
                else:
                    pass
    for l in col:
        print(*l)

def makeBombs(listBombs,w,h,n):
    list = []
    while len(listBombs) < n:
        a = random.randint(1,h)
        b = random.randint(1,w)
        list.append([a,b])
        [listBombs.append(x) for x in list if x not in listBombs]

def placeBombs(board,bombs,w,h):
    for i in bombs:
        board[i[0]][i[1]] = 'x'

def setBoard(board,bombs,w,h):
    for j in range(1, h+1):
        for k in range(1, w+1):
            if board[j][k] != 'x':
                bombsNear = 0
                for l in range(3):
                    for m in range(3):
                        if not l == m == 1 and board[j+l-1][k+m-1] == 'x':
                            bombsNear += 1
                board[j][k] = bombsNear

def setGame(board, hiddenBoard, bombs, w, h, num):
    makeBoard(board, w, h)
    makeBoard(hiddenBoard, w, h)
    makeBombs(bombs, w, h, num)
    placeBombs(board, bombs, w, h)
    setBoard(board, bombs, w, h)
    printBoard(hiddenBoard,w,h)

def askForInput():
    print('')
    f = input('Set Flag = 0, Click square = 1: '), input('Select row: '), input('Select collumn: ')
    f = [f[0][:1], f[1], f[2]]
    return f

def checkInput(board, f, w, h, b):
    if not (f[0].isalnum() and f[1].isalnum() and f[2].isalnum()):
        return False
    elif not (f[0].isdigit() and f[1].isdigit() and f[2].isdigit()):
        return False
    elif not (int(f[0]) == 0 or int(f[0]) == 1):
        return False
    elif int(f[1]) > h or int(f[2]) > w or int(f[1]) < 1 or int(f[2]) < 1:
        print('Out of range')
        return False
    elif not board[int(f[1])][int(f[2])] == '*':
        print('Square already opened ')
        openNeighbours(board, b, f)
        return True
    else:
        return True

def setFlag(board, f):
    if board[f[1]][f[2]] == '*':
        board[f[1]][f[2]] = ' '
    elif board[f[1]][f[2]] == ' ':
        board[f[1]][f[2]] = '*'

def selectSpace(hiddenBoard, board, f): #Blir ikke alltid brukt
    if hiddenBoard[f[1]][f[2]] != ' ':
        hiddenBoard[f[1]][f[2]] = board[f[1]][f[2]]
    if board[f[1]][f[2]] == 0:
        openNeighbours(hiddenBoard, board, f)

def openNeighbours(hiddenBoard, board, f):
    f = [int(f[0]), int(f[1]), int(f[2])]
    for i in range(-1,2,1):
        for j in range(-1,2,1):
            if hiddenBoard[f[1]][f[2]] != 0:
                if hiddenBoard[f[1]+i][f[2]+j] == ' ':
                    pass
                else:
                    hiddenBoard[f[1]+i][f[2]+j] = board[f[1]+i][f[2]+j]
            elif hiddenBoard[f[1]+i][f[2]+j] == '*':
                hiddenBoard[f[1]+i][f[2]+j] = board[f[1]+i][f[2]+j]
                selectSpace(hiddenBoard, board, [f[0], f[1]+i, f[2]+j])

def oneTurn(hiddenBoard, board, w, h):
    badInput = True
    while badInput:
        f = askForInput()
        c = checkInput(hiddenBoard, f, w, h, board)
        if c:
            g = [int(f[0]), int(f[1]), int(f[2])]
            if g[0] == 0:
                setFlag(hiddenBoard, g)
            elif g[0] == 1:
                selectSpace(hiddenBoard, board, g)
            badInput = False
    printBoard(hiddenBoard,w,h)
    if hiddenBoard[int(f[1])][int(f[2])] == 'x':
        cprint('OH NO! THE BOMB EXPLODED!!!!','red')
        return False
    else:
        return True

def onlyBombsLeft(hidden, board, w, h):
    bombsLeft = []
    for i in range(1, h+1):
        for j in range(1, w+1):
            if hidden[i][j] == '*' and board[i][j] == 'x':
                bombsLeft.append([i,j])
            elif hidden[i][j] == '*':
                return False
    for bomb in bombsLeft:
        hidden[bomb[0]][bomb[1]] = ' '
    print('Only bombs left on the board!')
    printBoard(hidden,w,h)
    cprint('You won!','green')
    return True

def allSpacesOpen(board, w, h):
    for i in range(1, h+1):
        for j in range(1, w+1):
            if board[i][j] == '*':
                return False
    print('You won!')
    return True

def main():
    setGame(theBoard, theHiddenBoard, listBombs, width, height, bombNumber)
    play = True
    while play:
        play = oneTurn(theHiddenBoard, theBoard, width, height)
        if allSpacesOpen(theHiddenBoard, width, height) or onlyBombsLeft(theHiddenBoard, theBoard, width, height):
            play = False

main()
