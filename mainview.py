try:
    from PyQt5.QtWidgets import (QWidget, QSizePolicy)
    from PyQt5.QtGui import (QPainter, QBrush, QColor, QPolygon)
    from PyQt5.QtCore import Qt
    from PyQt5 import QtCore
except:
    from PyQt4.QtGui import (QWidget, QSizePolicy, QPainter, QBrush, QColor, QPolygon)
    from PyQt4.QtCore import Qt
    from PyQt4 import QtCore
import numpy as np
import math


class MainView(QWidget):
    def __init__(self, parent, coords, blocks):
        super(MainView, self).__init__(parent)
        self.Model = blocks
        self.scale = 5
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, e):
        #print("Hello, world!")
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.fillRect(0, 0, w, h, QBrush(QColor(255, 255, 255)))
        self.displayLines(painter, w / 2, h / 2)

    def drawModel(self, b, p, x0, y0):
        s = self.scale
        r1 = math.sin(math.pi/2+0.5)
        r2 = math.cos(math.pi/2+0.5)
        rot_matrix = np.array([
            #[1,   0,  0, 0],
            #[0,   1,  0, 0],
            [ r1,  r2, 0, 0],
            [-r2,  r1, 0, 0],
            [  0,  0,  1, 0],
            [  0,  0,  0, 1]])
        rot_matrix2 = np.array([
            [  1,  0,  0, 0],
            [  0,  r2,  r1, 0],
            [  0,  -r1,  r2, 0],
            [  0,  0,  0, 1]])
        rot_matrix3 = np.array([
            [  1,  0,  0, 0],
            [  0,  1,  0, 0],
            [  0,  0,  r2, r1],
            [  0,  0,  -r1, r2]])
        rot_matrix = rot_matrix.dot(rot_matrix2).dot(rot_matrix)

        p1 = b.p1()
        p2 = np.array([b.p1()[0], b.p1()[1], b.p2()[2], 1])
        p3 = np.array([b.p1()[0], b.p2()[1], b.p2()[2], 1])
        p4 = np.array([b.p1()[0], b.p2()[1], b.p1()[2], 1])
        p5 = np.array([b.p2()[0], b.p1()[1], b.p1()[2], 1])
        p6 = np.array([b.p2()[0], b.p1()[1], b.p2()[2], 1])
        #p7 = np.array([b.p2()[0], b.p2()[1], b.p2()[2], 1])
        p7 = b.p2()
        p8 = np.array([b.p2()[0], b.p2()[1], b.p1()[2], 1])

        p1 = rot_matrix.dot(p1)
        p2 = rot_matrix.dot(p2)
        p3 = rot_matrix.dot(p3)
        p4 = rot_matrix.dot(p4)
        p5 = rot_matrix.dot(p5)
        p6 = rot_matrix.dot(p6)
        p7 = rot_matrix.dot(p7)
        p8 = rot_matrix.dot(p8)

        polygon = QPolygon([
            QtCore.QPoint(x0 +  s*p1[0], y0 - s*p1[1]),
            QtCore.QPoint(x0 +  s*p2[0], y0 - s*p2[1]),
            QtCore.QPoint(x0 +  s*p3[0], y0 - s*p3[1]),
            QtCore.QPoint(x0 +  s*p4[0], y0 - s*p4[1])
            ])
        p.drawConvexPolygon(polygon)

        polygon = QPolygon([
            QtCore.QPoint(x0 +  s*p5[0], y0 - s*p5[1]),
            QtCore.QPoint(x0 +  s*p6[0], y0 - s*p6[1]),
            QtCore.QPoint(x0 +  s*p7[0], y0 - s*p7[1]),
            QtCore.QPoint(x0 +  s*p8[0], y0 - s*p8[1])
            ])
        p.drawConvexPolygon(polygon)
        p.drawLine(x0 + s*p1[0], y0 - s*p1[1],
                x0 + s*p5[0], y0 - s*p5[1])
        p.drawLine(x0 + s*p2[0], y0 - s*p2[1],
                x0 + s*p6[0], y0 - s*p6[1])
        p.drawLine(x0 + s*p3[0], y0 - s*p3[1],
                x0 + s*p7[0], y0 - s*p7[1])
        p.drawLine(x0 + s*p4[0], y0 - s*p4[1],
                x0 + s*p8[0], y0 - s*p8[1])


    def displayLines(self, p, x0, y0):
        x0 = self.width() / 2
        y0 = self.height() / 2
        #p.setPen(Qt.NoPen)
        for b in self.Model:
            self.drawModel(b, p, x0, y0)
