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
    def __init__(self, parent):
        super(MainView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, e):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.fillRect(0, 0, w, h, QBrush(QColor(255, 255, 255)))
        self.displayLines(painter)

    def displayLines(self, p):
        x0 = self.width() / 2
        y0 = self.height() / 2
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(50, 50, 50)))
        test = QPolygon([
            QtCore.QPoint(100, 100),
            QtCore.QPoint(100, 200),
            QtCore.QPoint(200, 100)
        ])
        p.drawConvexPolygon(test)
        #p.drawLine(x0, y0, x0 - 50, y0 + 50)
        #p.drawLine(x0, y0, x0, y0 - 75)
        #p.drawLine(x0, y0, x0 + 75, y0)
