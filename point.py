import numpy as np
class MiniBlock:
    def __init__(self, p1, p2):
        self.value = np.array([p1, p2])

    def p1(self):
        return self.value[0]

    def p2(self):
        return self.value[1]
