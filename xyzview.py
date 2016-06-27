try:
    from PyQt5.QtWidgets import (QWidget, QSizePolicy)
    from PyQt5.QtGui import (QPainter, QBrush, QPen, QColor)
    from PyQt5.QtCore import (QPoint)
except:
    from PyQt4.QtGui import (QPainter, QBrush, QPen, QColor,
            QWidget, QSizePolicy)
    from PyQt4.QtCore import (QPoint)

from point import MiniBlock
import numpy as np


class XYZview(QWidget):
    def __init__(self, parent, blocks, coords):
        super(XYZview, self).__init__(parent)
        self.Model = blocks
        self.__scale = 5
        self.__resolution = 16
        self.__current_block = 0
        self.changing_point = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.coord1 = "xyz".find(coords[0])
        self.coord2 = "xyz".find(coords[1])

    def paintEvent(self, e):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.fillRect(0, 0, w, h, QBrush(QColor(255, 255, 255)))
        self.drawCoordLines(painter, w, h)
        self.drawModel(painter, w, h)

    def drawCoordLines(self, p, w, h):
        x0, y0 = w/2, h/2
        self.x0, self.y0 = x0, y0
        s = self.__scale
        p.setPen(QPen(QColor(240, 240, 240), 1))
        cx = cx1 = x0
        p.drawLine(x0, 0, x0, h)
        while (cx < w):
            cx += s
            cx1 -= s
            p.drawLine(cx, 0, cx, h)
            p.drawLine(cx1, 0, cx1, h)
        cy = cy1 = y0
        p.drawLine(0, y0, w, y0)
        while (cy < h):
            cy += s
            cy1 -= s
            p.drawLine(0, cy, w, cy)
            p.drawLine(cx1, cy1, w, cy1)
        p.setPen(QPen(QColor(250, 200, 200), 2))
        p.drawLine(x0, y0, x0, 0)
        p.drawLine(x0, y0, w, y0)
        p.setPen(QPen(QColor(50, 50, 50), 2))
        p.drawText(QPoint(w/2, 10), "XYZ"[self.coord2])
        p.drawText(QPoint(w-10, h/2), "XYZ"[self.coord1])
        p.setPen(QPen(QColor(200, 200, 200), 2))
        r = self.__resolution
        p.drawRect(x0 - self.__scale*r/2, y0 - self.__scale*r/2,
                   self.__scale*r, self.__scale*r)

    def drawModel(self, p, w, h):
        __scale = self.__scale
        p.setPen(QPen(QColor(50, 50, 50), 2))
        x0, y0 = w/2, h/2
        for b in self.Model:
            if b == self.__current_block:
                pass
            p.drawRect(x0 + __scale*b.p1()[self.coord1],
                    y0 - __scale*b.p1()[self.coord2],
                    __scale*b.p2()[self.coord1] - __scale*b.p1()[self.coord1],
                    __scale*b.p1()[self.coord2] - __scale*b.p2()[self.coord2])
        p.setPen(QPen(QColor(50, 150, 50), 2))
        if self.__current_block != 0:
            b = self.__current_block
            p.drawRect(x0 + __scale*b.p1()[self.coord1],
                    y0 - __scale*b.p1()[self.coord2],
                    __scale*b.p2()[self.coord1] - __scale*b.p1()[self.coord1],
                    __scale*b.p1()[self.coord2] - __scale*b.p2()[self.coord2])

    def mousePressEvent(self, e):
        if self.__current_block == 0:
            print("No current block")
            return
        c1 = int((e.pos().x() - self.x0) / self.__scale)
        c2 = int((self.y0 - e.pos().y()) / self.__scale)
        p1c1 = self.__current_block.p1()[self.coord1]
        p1c2 = self.__current_block.p1()[self.coord2]
        p2c1 = self.__current_block.p2()[self.coord1]
        p2c2 = self.__current_block.p2()[self.coord2]
        rr1 = ((c1 - p1c1)**2 + (c2 - p1c2)**2)
        rr2 = ((c1 - p1c1)**2 + (c2 - p2c2)**2)
        rr3 = ((c1 - p2c1)**2 + (c2 - p1c2)**2)
        rr4 = ((c1 - p2c1)**2 + (c2 - p2c2)**2)
        rrmin = min(rr1, rr2, rr3, rr4)
        print(rr1, rr2, rr3, rr4)
        print(rrmin)
        if (rrmin < 100):
            if rrmin == rr1:
                self.changing_point = 1
            elif rrmin == rr2:
                self.changing_point = 2
            elif rrmin == rr3:
                self.changing_point = 3
            elif rrmin == rr4:
                self.changing_point = 4
            else:
                self.changing_point = 0
            return
        else:
            self.changing_point = 5 # no point selected

    def mouseMoveEvent(self, e):
        c1 = int((e.pos().x() - self.x0) / self.__scale)
        c2 = int((self.y0 - e.pos().y()) / self.__scale)
        if self.changing_point == 1:
            self.__current_block.p1()[self.coord1] = c1
            self.__current_block.p1()[self.coord2] = c2
        elif self.changing_point == 2:
            self.__current_block.p1()[self.coord1] = c1
            self.__current_block.p2()[self.coord2] = c2
        elif self.changing_point == 3:
            self.__current_block.p2()[self.coord1] = c1
            self.__current_block.p1()[self.coord2] = c2
        elif self.changing_point == 4:
            self.__current_block.p2()[self.coord1] = c1
            self.__current_block.p2()[self.coord2] = c2
        elif self.changing_point == 5:
            print("something")
        self.parent().update()

    def set_resolution(self, v):
        self.__resolution = v

    def set_scale(self, v):
        self.__scale = v

    def set_current_block(self, v):
        self.__current_block = v
