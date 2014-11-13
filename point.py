import numpy as np


class MiniBlock:
    def __init__(self, p1, p2):
        self.value = np.array([p1, p2])

    def p1(self):
        return self.value[0]

    def p2(self):
        return self.value[1]

    def turnX(self):
        self.value[0][0]*=-1
        self.value[1][0]*=-1

    def turnY(self):
        self.value[0][1]*=-1
        self.value[1][1]*=-1

    def turnZ(self):
        self.value[0][2]*=-1
        self.value[1][2]*=-1

    def swapXY(self):
        self.value[0][0], self.value[0][1] = self.value[0][1], self.value[0][0]
        self.value[1][0], self.value[1][1] = self.value[1][1], self.value[1][0]

    def swapXZ(self):
        self.value[0][0], self.value[0][2] = self.value[0][2], self.value[0][0]
        self.value[1][0], self.value[1][2] = self.value[1][2], self.value[1][0]

    def swapYZ(self):
        self.value[0][1], self.value[0][2] = self.value[0][2], self.value[0][1]
        self.value[1][1], self.value[1][2] = self.value[1][2], self.value[1][1]
