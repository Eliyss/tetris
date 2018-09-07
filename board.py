from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor 
import sys, random
import blocks
import shapes

# we want a pause, play, hold/swap, next shape, score, rotate bounce

class tetris(QMainWindow)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.gameboard = board(self)

class board(QFrame):
    boardWidth = 10
    boardHeight = 22
    tickRate = 500
    squareSize = 50

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
    
    def initBoard(self):
        self.currentShape = blocks.Shape()
        self.squareGrid = [][]
        self.currentX = 0
        self.currentY = 0
       

    def getShapeAt(self, x, y):
        return self.squareGrid[x][y]
    
    def setShapeAt(self, x, y, shape):
        self.squareGrid[x][y] = shape

    def spawnShape(self):
        self.currentShape = blocks.Shape()
        self.currentShape.setRandomShape
        self.currentX = 4
        self.currentY = 20
        self.totalLinesCleared = 0

        if not self.placeBlock(self.currentShape, self.currentX, self.currentY):
            #game is over
    
    def placeBlock(self, shape, newX, newY):
        for i in range(4):
            x = newX + shape.getX(i)
            y = newX + shape.getY(i)

            if x < 0 or x > 9 or y < 0 or y > 21:
                return False
            if self.getShapeAt(x, y) != blocks.empty:
                return False
            
        self.currentShape = shape
        self.currentX = newX
        self.currentY = newY
        self.updateBoard()

       return True
    
    def downOne(self):
        if not self.placeBlock(self.curPiece, self.curX, self.curY - 1):
            self.reachedBottom()

    def smash(self):
        tempY = self.currentY
        while tempT > 0:
            if placeBlock(self.currentShape, self.currentX, tempY-1):
                tempY -= 1
            else:
                break

        self.reachedBottom()
    
    def reachedBottom(self):
        for i in range(4):
            x = self.currentX + self.currentShape.getX()
            y = self.currentY + self.currentShape.getY()
            self.setShapeAt(x, y, self.currentShape)

            self.clearLines()

            self.spawnShape()
    
    def clearLines(self):
        fullRows = []
        linesCleared = 0

        for i in range(20):
            full = True
            for j in range(10):
                if self.getShapeAt(j, i) = blocks.empty:
                    full = False

            if full:
                fullRows.append(i)
                linesCleared += 1
            
        for i in fullRows:
            for j in range(i, 20):
                for k in range(10):
                    self.setShapeAt(k, j, self.getShapeAt(k, j+1))

        if linesCleared > 0:
            self.totalLinesCleared += 1
            self.update()
           

    def drawSquare(self, painter, x, y, shape):        
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, 50 - 2, 
            50 - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + 50 - 1, x, y)
        painter.drawLine(x, y, x + 50 - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + 50 - 1,
            x + 50 - 1, y + 50 - 1)
        painter.drawLine(x + 50 - 1, 
            y + 50 - 1, x + 50 - 1, y + 1)


