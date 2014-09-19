from PyQt5.QtWidgets import (QDialog, QPushButton, QGridLayout,
                             QFileDialog, QSpinBox, QLabel, QSpacerItem,
                             QSizePolicy)
from point import Point


class NewProjectDialog(QDialog):
    def __init__(self, parent):
        super(NewProjectDialog, self).__init__(parent)
        self.project_file = ""
        self.createGUI()
        self.connectSlots()

    def actionOK(self):
        self.project_file = QFileDialog.getSaveFileName(self, "Save file")[0]
        print(self.project_file)
        self.parent().project_file = self.project_file

        self.parent().projectData.centralBlock = Point(0, 0, 0)
        self.close()

    def actionCancel(self):
        self.close()

    def createGUI(self):
        self.grLayout1 = QGridLayout()
        self.spX = QSpinBox()
        self.spX.setMinimum(1)
        self.spX.setMaximum(5)
        self.spY = QSpinBox()
        self.spY.setMinimum(1)
        self.spY.setMaximum(5)
        self.spZ = QSpinBox()
        self.spZ.setMinimum(1)
        self.spZ.setMaximum(5)
        self.pbSaveAs = QPushButton("Save as", self)
        self.pbCancel = QPushButton("Cancel", self)
        self.grLayout1.addWidget(QLabel("X size"), 0, 0)
        self.grLayout1.addWidget(self.spX, 1, 0)
        self.grLayout1.addWidget(QLabel("Y size"), 0, 1)
        self.grLayout1.addWidget(self.spY, 1, 1)
        self.grLayout1.addWidget(QLabel("Z size"), 0, 2)
        self.grLayout1.addWidget(self.spZ, 1, 2)
        self.grLayout1.addWidget(self.pbSaveAs, 10, 0)
        self.grLayout1.addWidget(self.pbCancel, 10, 1)
        self.grLayout1.addItem(QSpacerItem(5, 200, QSizePolicy.Minimum,
                                           QSizePolicy.Expanding), 15, 0, 1, 1)
        self.setLayout(self.grLayout1)

        self.setWindowTitle("Create new project")
        self.resize(600, 400)

    def connectSlots(self):
        self.pbSaveAs.clicked.connect(self.actionOK)
        self.pbCancel.clicked.connect(self.actionCancel)
