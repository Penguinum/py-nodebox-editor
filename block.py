import numpy as np


class Block(object):
    coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, p1, p2):
        self.value = np.array([p1, p2])

    def p1(self):
        return self.value[0]

    def p2(self):
        return self.value[1]

    def turn(self, coord):
        for p in (0, 1):
            self.value[p][self.coord[coord]] *= -1

    def swap(self, coords):
        (c1, c2) = (self.coord[c] for c in coords)
        for p in (0, 1):
            self.value[p][c1], self.value[p][c2] = self.value[p][c2], self.value[p][c1]

