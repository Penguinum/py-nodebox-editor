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
from math import sin, cos, pi


class MainView(QWidget):
    def __init__(self, parent, coords, blocks):
        super(MainView, self).__init__(parent)
        self.Model = blocks
        self.scale = 2
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0
        self.rotation = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

    def paintEvent(self, e):
        #print("Hello, world!")
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.fillRect(0, 0, w, h, QBrush(QColor(255, 255, 255)))
        self.displayLines(painter, w / 2, h / 2)

    def mousePressEvent(self, e):
        self.curX = e.pos().x()
        self.curZ = e.pos().y()
        self.update()

    def mouseMoveEvent(self, e):
        self.rotX += (e.pos().x() - self.curX)*0.01
        self.rotZ += (e.pos().y() - self.curZ)*0.01
        self.curX = e.pos().x()
        self.curZ = e.pos().y()
        self.recalcRotation()
        self.update()

    def wheelEvent(self, e):
        self.rotY+=e.delta()*0.001
        self.recalcRotation()
        self.update()

    def recalcRotation(self):
        my = np.array([
            [cos(self.rotY), -sin(self.rotY), 0, 0],
            [sin(self.rotY),  cos(self.rotY), 0, 0],
            [             0,               0, 1, 0],
            [             0,               0, 0, 1]])
        mx = np.array([
            [ cos(self.rotX), 0, sin(self.rotX), 0],
            [              0,              1, 0, 0],
            [-sin(self.rotX), 0, cos(self.rotX), 0],
            [              0,              0, 0, 1]])
        mz = np.array([
            [1,              0,               0, 0],
            [0, cos(self.rotZ), -sin(self.rotZ), 0],
            [0, sin(self.rotZ),  cos(self.rotZ), 0],
            [0,              0,               0, 1]])
        self.rotation = mx.dot(my.dot(mz))

    def drawModel(self, b, p, x0, y0):
        s = self.scale
        r1 = sin(pi/2+0.5)
        r2 = cos(pi/2+0.5)

        p1 = b.p1()
        p2 = np.array([b.p1()[0], b.p1()[1], b.p2()[2], 1])
        p3 = np.array([b.p1()[0], b.p2()[1], b.p2()[2], 1])
        p4 = np.array([b.p1()[0], b.p2()[1], b.p1()[2], 1])
        p5 = np.array([b.p2()[0], b.p1()[1], b.p1()[2], 1])
        p6 = np.array([b.p2()[0], b.p1()[1], b.p2()[2], 1])
        #p7 = np.array([b.p2()[0], b.p2()[1], b.p2()[2], 1])
        p7 = b.p2()
        p8 = np.array([b.p2()[0], b.p2()[1], b.p1()[2], 1])

        p1 = self.rotation.dot(p1)
        p2 = self.rotation.dot(p2)
        p3 = self.rotation.dot(p3)
        p4 = self.rotation.dot(p4)
        p5 = self.rotation.dot(p5)
        p6 = self.rotation.dot(p6)
        p7 = self.rotation.dot(p7)
        p8 = self.rotation.dot(p8)

        c1,c2 = 0, 1
        polygon = QPolygon([
            QtCore.QPoint(x0 +  s*p1[c1], y0 - s*p1[c2]),
            QtCore.QPoint(x0 +  s*p2[c1], y0 - s*p2[c2]),
            QtCore.QPoint(x0 +  s*p3[c1], y0 - s*p3[c2]),
            QtCore.QPoint(x0 +  s*p4[c1], y0 - s*p4[c2])
            ])
        p.drawConvexPolygon(polygon)

        polygon = QPolygon([
            QtCore.QPoint(x0 +  s*p5[c1], y0 - s*p5[c2]),
            QtCore.QPoint(x0 +  s*p6[c1], y0 - s*p6[c2]),
            QtCore.QPoint(x0 +  s*p7[c1], y0 - s*p7[c2]),
            QtCore.QPoint(x0 +  s*p8[c1], y0 - s*p8[c2])
            ])
        p.drawConvexPolygon(polygon)
        p.drawLine(x0 + s*p1[c1], y0 - s*p1[c2],
                x0 +    s*p5[c1], y0 - s*p5[c2])
        p.drawLine(x0 + s*p2[c1], y0 - s*p2[c2],
                x0 +    s*p6[c1], y0 - s*p6[c2])
        p.drawLine(x0 + s*p3[c1], y0 - s*p3[c2],
                x0 +    s*p7[c1], y0 - s*p7[c2])
        p.drawLine(x0 + s*p4[c1], y0 - s*p4[c2],
                x0 +    s*p8[c1], y0 - s*p8[c2])


    def displayLines(self, p, x0, y0):
        x0 = self.width() / 2
        y0 = self.height() / 2
        #p.setPen(Qt.NoPen)
        for b in self.Model:
            self.drawModel(b, p, x0, y0)
