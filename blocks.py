from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor 
import sys, random

class Shape(object):
    shapeCoords =   (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    empty = 0
    Z = 1
    S = 2
    L = 3
    T = 4
    O = 5
    L = 6
    J = 7


    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]
        self.shapeType = self.empty
        self.setShape(Shape.empty)


    def getShape(self):
        return self.shapeType
    
    def setShape(self, shape):
        coords = Shape.shapeCoords[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = coords[i][j]
        
        self.shapeType = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def getX(self, i):
        return self.coords[i][0]

    def setX(self, i, newX):
        self.coords[i][0] = newX

    def getY(self, i):
        return self.coords[i][1]

    def setY(self, i, newY):
        self.coords[i][1] = newY

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])
        return m

    def rotateRight(self):
        if self.shapeType == Shape.O:
            return self

        rotated = Shape()
        rotated.shapeType = self.shapeType
        
        for i in range(4):
            rotated.setX(i, -self.getY(i))
            rotated.setY(i, self.getX(i))
            
        return rotated

    def rotateLeft(self):
        if self.shapeType == Shape.O:
            return self

        rotated = Shape()
        rotated.shapeType = self.shapeType
        
        for i in range(4):
            rotated.setX(i, self.getY(i))
            rotated.setY(i, -self.getX(i))

        return rotated
