try:
    from PyQt5.QtWidgets import (QWidget, QSizePolicy)
    from PyQt5.QtGui import (QPainter, QBrush, QPen, QColor)
    from PyQt5.QtCore import (QPoint)
except:
    from PyQt4.QtGui import (QPainter, QBrush, QPen, QColor, QWidget, QSizePolicy)
    from PyQt4.QtCore import (QPoint)

from point import MiniBlock


class XYZview(QWidget):
    def __init__(self, parent, coords, blocks):
        super(XYZview, self).__init__(parent)
        self.coords = coords
        self.Model = blocks
        self.scale = 5
        self.current_block = 0
        self.changing_point = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        s = self.scale
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
        if self.coords == "XY":
            p.drawText(QPoint(w/2, 10), "Y")
            p.drawText(QPoint(w-10, h/2), "X")
        elif self.coords == "YZ":
            p.drawText(QPoint(w/2, 10), "Y")
            p.drawText(QPoint(w-10, h/2), "Z")
        elif self.coords == "XZ":
            p.drawText(QPoint(w/2, 10), "Z")
            p.drawText(QPoint(w-10, h/2), "X")
        p.setPen(QPen(QColor(200, 200, 200), 2))
        p.drawRect(x0 - self.scale*8, y0 - self.scale*8,
                   self.scale*16, self.scale*16)

    def drawModel(self, p, w, h):
        scale = self.scale
        p.setPen(QPen(QColor(50, 50, 50), 2))
        x0, y0 = w/2, h/2
        for b in self.Model:
            if b == self.current_block:
                pass
            if (self.coords == "XY"):
                p.drawRect(x0 + scale*b.p1.x, y0 - scale*b.p1.y,
                           scale*b.p2.x-scale*b.p1.x, scale*b.p1.y-scale*b.p2.y)
            elif (self.coords == "YZ"):
                p.drawRect(x0 + scale*b.p1.z, y0 - scale*b.p1.y,
                           scale*b.p2.z-scale*b.p1.z, scale*b.p1.y-scale*b.p2.y)
            elif (self.coords == "XZ"):
                p.drawRect(x0 + scale*b.p1.x, y0 - scale*b.p1.z,
                           scale*b.p2.x-scale*b.p1.x, scale*b.p1.z-scale*b.p2.z)
        p.setPen(QPen(QColor(50, 150, 50), 2))

        if self.current_block != 0:
            b = self.current_block
            if (self.coords == "XY"):
                p.drawRect(x0 + scale*b.p1.x, y0 - scale*b.p1.y,
                           scale*b.p2.x-scale*b.p1.x, scale*b.p1.y-scale*b.p2.y)
            elif (self.coords == "YZ"):
                p.drawRect(x0 + scale*b.p1.z, y0 - scale*b.p1.y,
                           scale*b.p2.z-scale*b.p1.z, scale*b.p1.y-scale*b.p2.y)
            elif (self.coords == "XZ"):
                p.drawRect(x0 + scale*b.p1.x, y0 - scale*b.p1.z,
                           scale*b.p2.x-scale*b.p1.x, scale*b.p1.z-scale*b.p2.z)

    def mousePressEvent(self, e):
        if self.current_block == 0:
            print("No current block")
            return
        c1 = int((e.pos().x() - self.x0) / self.scale)
        c2 = int((self.y0 - e.pos().y()) / self.scale)
        if self.coords == "XY":
            p1c1 = self.current_block.p1.x
            p1c2 = self.current_block.p1.y
            p2c1 = self.current_block.p2.x
            p2c2 = self.current_block.p2.y
        elif self.coords == "XZ":
            p1c1 = self.current_block.p1.x
            p1c2 = self.current_block.p1.z
            p2c1 = self.current_block.p2.x
            p2c2 = self.current_block.p2.z
        elif self.coords == "YZ":
            p1c1 = self.current_block.p1.y
            p1c2 = self.current_block.p1.z
            p2c1 = self.current_block.p2.y
            p2c2 = self.current_block.p2.z
        rr1 = ((c1 - p1c1)**2 + (c2 - p1c2)**2)
        rr2 = ((c1 - p1c1)**2 + (c2 - p2c2)**2)
        rr3 = ((c1 - p2c1)**2 + (c2 - p1c1)**2)
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
            self.changing_point = 5


    def mouseMoveEvent(self, e):
        c1 = int((e.pos().x() - self.x0) / self.scale)
        c2 = int((self.y0 - e.pos().y()) / self.scale)
        if self.coords == "XY":
            if self.changing_point == 1:
                self.current_block.p1.x = c1
                self.current_block.p1.y = c2
            elif self.changing_point == 2:
                self.current_block.p1.x = c1
                self.current_block.p2.y = c2
            elif self.changing_point == 3:
                self.current_block.p2.x = c1
                self.current_block.p1.y = c2
            elif self.changing_point == 4:
                self.current_block.p2.x = c1
                self.current_block.p2.y = c2
            elif self.changing_point == 5:
                print("something")
        elif self.coords == "XZ":
            if self.changing_point == 1:
                self.current_block.p1.x = c1
                self.current_block.p1.z = c2
            elif self.changing_point == 2:
                self.current_block.p1.x = c1
                self.current_block.p2.z = c2
            elif self.changing_point == 3:
                self.current_block.p2.x = c1
                self.current_block.p1.z = c2
            elif self.changing_point == 4:
                self.current_block.p2.x = c1
                self.current_block.p2.z = c2
            elif self.changing_point == 5:
                print("something")
        elif self.coords == "YZ":
            if self.changing_point == 1:
                self.current_block.p1.z = c1
                self.current_block.p1.y = c2
            elif self.changing_point == 2:
                self.current_block.p1.z = c1
                self.current_block.p2.y = c2
            elif self.changing_point == 3:
                self.current_block.p2.z = c1
                self.current_block.p1.y = c2
            elif self.changing_point == 4:
                self.current_block.p2.z = c1
                self.current_block.p2.y = c2
            elif self.changing_point == 5:
                print("something")
        self.parent().update()
