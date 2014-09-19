from PyQt5.QtWidgets import (QWidget, QSizePolicy)
from PyQt5.QtGui import (QPainter, QBrush, QColor)


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
        p.drawLine(x0, y0, x0 - 50, y0 + 50)
        p.drawLine(x0, y0, x0, y0 - 75)
        p.drawLine(x0, y0, x0 + 75, y0)
