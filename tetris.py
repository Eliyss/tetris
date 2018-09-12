from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor 
import sys, random
import board

class Tetris(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):    
        self.tboard = board.Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)
        
        self.tboard.start()
        
        self.resize(200, 440)
        self.center()
        self.setWindowTitle('Tetris')        
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()    
    sys.exit(app.exec_())