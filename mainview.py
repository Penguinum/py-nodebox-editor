from point import *

from OpenGL.GL import *
from PyQt5.QtOpenGL import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainView(QGLWidget):
    def __init__(self, parent):
        super(MainView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
