from point import *


class model:
    def __init__(self):
        self.parts = []
        self.centralPoint = Point(0, 0, 0)

    def addPart(self, x1, y1, z1, x2, y2, z2):
        self.parts.append(MiniBlock(Point(x1, y1, z1), Point(x2, y2, z2)))

    def addMiniBlock(self, mb):
        self.parts.append(mb)
