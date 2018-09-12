from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor 
import sys, random, blocks

class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    boardWidth = 10
    boardHeight = 22
    tickRate = 300
    squareSize = 20

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        
    def initBoard(self):     
        self.timer = QBasicTimer()
        self.clearingLines = False
        
        self.currentX = 0
        self.currentY = 0
        self.totalRemovedLines = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.resetGame()
        
    def getShapeAt(self, x, y):
        return self.board[(y * Board.boardWidth) + x]

        
    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.boardWidth) + x] = shape

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.clearingLines = False
        self.totalRemovedLines = 0
        self.resetGame()

        self.msg2Statusbar.emit(str(self.totalRemovedLines))

        self.spawnBlock()
        self.timer.start(Board.tickRate, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")  
        else:
            self.timer.start(Board.tickRate, self)
            self.msg2Statusbar.emit(str(self.totalRemovedLines))
        self.update()

        
    def paintEvent(self, event):        
        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.boardHeight * Board.squareSize

        for i in range(Board.boardHeight):
            for j in range(Board.boardWidth):
                shape = self.getShapeAt(j, Board.boardHeight - i - 1)
                
                if shape != blocks.Shape.empty:
                    self.drawSquare(painter,
                        rect.left() + j * Board.squareSize,
                        boardTop + i * Board.squareSize, shape)

        if self.currentBlock.getShape() != blocks.Shape.empty:
            for i in range(4):
                x = self.currentX + self.currentBlock.getX(i)
                y = self.currentY - self.currentBlock.getY(i)
                self.drawSquare(painter, rect.left() + x * Board.squareSize,
                    boardTop + (Board.boardHeight - y - 1) * Board.squareSize,
                    self.currentBlock.getShape())
                    
    def keyPressEvent(self, event):
        if not self.isStarted or self.currentBlock.getShape() == blocks.Shape.empty:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == Qt.Key_P:
            self.pause()
            return
            
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.placeBlock(self.currentBlock, self.currentX - 1, self.currentY)
        elif key == Qt.Key_Right:
            self.placeBlock(self.currentBlock, self.currentX + 1, self.currentY)
        elif key == Qt.Key_Down:
            self.placeBlock(self.currentBlock.rotateRight(), self.currentX, self.currentY)           
        elif key == Qt.Key_Up:
            self.placeBlock(self.currentBlock.rotateLeft(), self.currentX, self.currentY)   
        elif key == Qt.Key_Space:
            self.smash()   
        elif key == Qt.Key_D:
            self.downOne()
        else:
            super(Board, self).keyPressEvent(event)
                
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.clearingLines:
                self.clearingLines = False
                self.spawnBlock()
            else:
                self.downOne()   
        else:
            super(Board, self).timerEvent(event)
            
    def resetGame(self):
        for i in range(Board.boardHeight * Board.boardWidth):
            self.board.append(blocks.Shape.empty)
 
    def smash(self):
        newY = self.currentY
        
        while newY > 0:
            
            if not self.placeBlock(self.currentBlock, self.currentX, newY - 1):
                break
                
            newY -= 1

        self.reachedBottom()
        

    def downOne(self):
        if not self.placeBlock(self.currentBlock, self.currentX, self.currentY - 1):
            self.reachedBottom()
            

    def reachedBottom(self):
        for i in range(4):
            
            x = self.currentX + self.currentBlock.getX(i)
            y = self.currentY - self.currentBlock.getY(i)
            self.setShapeAt(x, y, self.currentBlock.getShape())

        self.clearLines()

        if not self.clearingLines:
            self.spawnBlock()
            

    def clearLines(self):
        linesCleared = 0
        fullLines = []

        for i in range(Board.boardHeight):
            full = True
            for j in range(Board.boardWidth):
                if self.getShapeAt(j, i) == blocks.Shape.empty:
                    full = False
                    break

            if full:
                fullLines.append(i)

        fullLines.reverse()
        
        for m in fullLines:
            for k in range(m, Board.boardHeight):
                for l in range(Board.boardWidth):
                        self.setShapeAt(l, k, self.getShapeAt(l, k + 1))

        linesCleared = linesCleared + len(fullLines)

        if linesCleared > 0:
            self.totalRemovedLines = self.totalRemovedLines + linesCleared
            self.msg2Statusbar.emit(str(self.totalRemovedLines))
            self.clearingLines = True
            self.currentBlock.setShape(blocks.Shape.empty)
            self.update()

    def spawnBlock(self):
        self.currentBlock = blocks.Shape()
        self.currentBlock.setRandomShape()
        self.currentX = Board.boardWidth // 2 + 1
        self.currentY = Board.boardHeight - 1 + self.currentBlock.minY()
        
        if not self.placeBlock(self.currentBlock, self.currentX, self.currentY):
            self.currentBlock.setShape(blocks.Shape.empty)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")

    def placeBlock(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.getX(i)
            y = newY - newPiece.getY(i)
            
            if x < 0 or x >= Board.boardWidth or y < 0 or y >= Board.boardHeight:
                return False
                
            if self.getShapeAt(x, y) != blocks.Shape.empty:
                return False

        self.currentBlock = newPiece
        self.currentX = newX
        self.currentY = newY
        self.update()
        
        return True

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, Board.squareSize - 2, 
            Board.squareSize - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + Board.squareSize - 1, x, y)
        painter.drawLine(x, y, x + Board.squareSize - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + Board.squareSize - 1,
            x + Board.squareSize - 1, y + Board.squareSize - 1)
        painter.drawLine(x + Board.squareSize - 1, 
            y + Board.squareSize - 1, x + Board.squareSize - 1, y + 1)
