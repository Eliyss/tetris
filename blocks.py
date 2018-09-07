from PyQt5.q

class Shape(object):
    shapeCoords =   (
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

    empty = 0
    I = 1
    J = 2
    L = 3
    O = 4
    S = 5
    T = 6
    Z = 7


    def __init__(self):
        self.shape = empty
        self.coords = [[0, 0] for i in range(4)]


    def getShape(self):
        return self.shape
    
    def setShape(self, shape):
        self.shape = shape
        coords = shapeCoords[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = coords[i][j]

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

    def rotateRight(self):
        if self.shape == O:
            return self
        else if self.shap

        rotated = block()
        rotated.shape = self.shape

        for i in range(4):
            rotated.