try:
    from PyQt5.QtWidgets import (QWidget, QSizePolicy)
    from PyQt5.QtGui import (QPainter, QBrush, QColor, QPolygon)
    from PyQt5.QtCore import Qt
    from PyQt5 import QtCore
except:
    from PyQt4.QtGui import (QWidget, QSizePolicy, QPainter, QBrush, QColor, QPolygon)
    from PyQt4.QtCore import Qt
    from PyQt4 import QtCore


class MainView(QWidget):
    def __init__(self, parent, coords, blocks):
        super(MainView, self).__init__(parent)
        self.Model = blocks
        self.scale = 5
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, e):
        print("Hello, world!")
        #painter = QPainter(self)
        #w = self.width()
        #h = self.height()
        #painter.fillRect(0, 0, w, h, QBrush(QColor(255, 255, 255)))
        #self.displayLines(painter, w / 2, h / 2)

    def drawModel(self, b, p, x0, y0):
        s = self.scale
        p.setBrush(QBrush(QColor(180, 230, 180)))
        polygon = QPolygon([
            QtCore.QPoint(x0 + s*b.p1.x, y0 - s*b.p1.z),
            QtCore.QPoint(x0 + s*b.p2.x, y0 - s*b.p1.z),
            QtCore.QPoint(x0 + s*b.p2.x, y0 - s*b.p2.z),
            QtCore.QPoint(x0 + s*b.p1.x, y0 - s*b.p2.z)
            ])
        p.drawConvexPolygon(polygon)

    def displayLines(self, p, x0, y0):
        x0 = self.width() / 2
        y0 = self.height() / 2
        #p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(200, 250, 200)))
        for b in self.Model:
            self.drawModel(b, p, x0, y0)
        #p.drawConvexPolygon(test) 
        #p.drawLine(x0, y0, x0 - 50, y0 + 50)
        #p.drawLine(x0, y0, x0, y0 - 75)
        #p.drawLine(x0, y0, x0 + 75, y0)
