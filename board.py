from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor 
import sys, random
import blocks


# we want a pause, play, hold/swap, next shape, score, rotate bounce

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
        self.squareGrid = []
        self.currentX = 0
        self.currentY = 0
        self.isStarted = False
        self.isPaused = False
        self.totalLinesCleared = 0
        self.resetBoard()
        self.clearingLines = False
        self.setFocusPolicy(Qt.StrongFocus)
        self.timer = QBasicTimer()

    def keyPressEvent(self, event):
        if not self.isStarted or self.currentPiece.shape() == blocks.empty:
            super(board, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == Qt.Key_P:
            self.pause()
            return
            
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.placeBlock(self.currentShape, self.currentX-1, self.currentY)
        elif key == Qt.Key_Right:
            self.placeBlock(self.currentShape, self.currentX+1, self.currentY) 
        elif key == Qt.Key_Down:
            self.placeBlock(self.currentShape.rotateRight(), self.currentX, self.currentY)         
        elif key == Qt.Key_Up:
            self.placeBlock(self.currentShape.rotateLeft(), self.currentX, self.currentY)           
        elif key == Qt.Key_Space:
            self.smash()
        elif key == Qt.Key_D:
            self.downOne()
        else:
            super(board, self).keyPressEvent(event)
                

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            
            if self.clearingLines:
                self.clearingLines = False
                self.newPiece()
            else:
                self.downOne()
                
        else:
            super(board, self).timerEvent(event)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.totalLinesCleared = 0
        self.resetBoard()

       # self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.spawnShape()
        self.timer.start(board.tickRate, self)

        
    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
 #           self.msg2Statusbar.emit("paused")
            
        else:
            self.timer.start(board.tickRate, self)
#            self.msg2Statusbar.emit(str(self.totalLinesCleared))

        self.update()
    
    def resetBoard(self):
        self.squareGrid = []
        for i in range(220):
            self.squareGrid.append(0)
      

    def getShapeAt(self, x, y):
        return self.squareGrid[x*y + y]
    
    def setShapeAt(self, x, y, shape):
        self.squareGrid[x*y+y] = shape

    def spawnShape(self):
        self.currentShape = blocks.Shape()
        self.currentShape.setRandomShape()
        self.currentX = 4
        self.currentY = 20
        self.totalLinesCleared = 0

        if not self.placeBlock(self.currentShape, self.currentX, self.currentY):
            #game is over
            return
    
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
        self.update()

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

            if not self.clearingLines:
                self.spawnShape()
    
    def clearLines(self):
        fullRows = []
        linesCleared = 0

        for i in range(20):
            full = True
            for j in range(10):
                if self.getShapeAt(j, i) == blocks.empty:
                    full = False

            if full:
                fullRows.append(i)
                linesCleared += 1
            
        for i in fullRows:
            for j in range(i, 20):
                for k in range(10):
                    self.setShapeAt(k, j, self.getShapeAt(k, j+1))

        if linesCleared > 0:
            self.totalLinesCleared += linesCleared
            self.clearingLines = True
            self.currentShape.setShape(blocks.empty)
            self.update()


    def drawSquare(self, painter, x, y, shape):
        colors = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                  0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        
        color = QColor(colors[shape])
        painter.fillRect(x+1, y+1, 48, 48, color)

        painter.setPen(color.lighter)
        painter.drawLine(x, y, x, y+50)
        painter.drawLine(x, y+50, x+50, y+50)

        painter.setPen(color.darker)
        painter.drawLine(x, y, x+50, y)
        painter.drawLine(x+50, y, x+50, y+50)

    def drawBox(self, painter, x, y):
        color = QColor(0xFFFFFF)
        painter.setPen(color)
        painter.drawLine(x, y, x, y+50)
        painter.drawLine(x, y+50, x+50, y+50)
        painter.drawLine(x, y, x+50, y)
        painter.drawLine(x+50, y, x+50, y+50)


    def updateBoard(self, event):
        painter = QPainter(self)
        for i in range(22):
            for j in range(10):
                shape = self.getShapeAt(j, i)

                if shape == blocks.empty:
                    self.drawBox(painter, j*50, i*50)
                else:
                    self.drawSquare(painter, j*50, i*50, shape)

        if self.currentShape.shape() != board.empty:
            for i in range(4):
                x = self.currentX + self.currentShape.getX(i)
                y = self.currentY + self.currentShape.getY(i)
                self.drawSquare(painter, x*50, y*50, self.currentShape.shape)

                    
