from PyQt5.q

class block(object):
    blockCoords =   (
        ((0, 0),    (0, 0),     (0, 0),     (0, 0)),
        ((-1, 0),   (0, 0),     (1, 0),     (2, 0)), #I
        ((-1, 1),   (-1, 0),    (0, 0),     (1, 0)),
        ((-1, 0),   (0, 0),     (1, 0),     (1, 1)),
        ((0, 0),    (1, 0),     (1, 1),     (0, 1)), #O
        ((-1, 0),   (0, 0),     (0, 1),     (1, 1)),
        ((-1, 0),   (0, 0),     (0, 1),     (1, 0)),
        ((-1, 1),   (0, 1),     (0, 0),     (1, 0)),
        ((0, 0),    (0, 0),     (0, 0),     (0, 0))
    )

    blankShape = 0
    I = 1
    J = 2
    L = 3
    O = 4
    S = 5
    T = 6
    Z = 7


    def __init__(self):
        self.shape = blankShape
        self.coords = [[0, 0] for i in range(4)]


    def getShape(self):
        return self.shape
    
    def createShape(self, shape):
        self.shape = shape
        coords = blockCoords[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = coords[i][j]

    def height(self):
        



    def rotateRight(self):
        if self.shape == O:
            return self
        else if self.shap

        rotated = block()
        rotated.shape = self.shape

        for i in range(4):
            rotated.


