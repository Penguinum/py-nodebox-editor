#!/usr/bin/env python3

try:
    from PyQt5.QtWidgets import (QPushButton, QGridLayout, QWidget, QApplication,
                                 QLabel, QMenuBar, QVBoxLayout,
                                 QHBoxLayout, QMainWindow, QFileDialog, QComboBox,
                                 QSpacerItem, QSizePolicy, QSlider)
    from PyQt5.QtCore import Qt
    is_qt5 = True
except:
    from PyQt4.QtGui import (QPushButton, QGridLayout, QWidget, QApplication,
                                 QLabel, QMenuBar, QVBoxLayout,
                                 QHBoxLayout, QMainWindow, QFileDialog, QComboBox,
                                 QSpacerItem, QSizePolicy, QSlider)
    
    from PyQt4.QtCore import Qt
    is_qt5 = False

import sys
import codegen
from xyzview import XYZview
from mainview import MainView
from point import MiniBlock, Point


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.parts = []
        self.miniblocks = []
        self.centralBlock = Point(0, 0, 0)
        self.createGUI()
        self.createMenu()
        self.connectSlots()
        self.project_file = ""
        self.current_block = 0


    def createGUI(self):
        self.widget = QWidget(self)
        self.gvMain = MainView(self)
        self.gvX = XYZview(self, "YZ", self.miniblocks)
        self.gvY = XYZview(self, "XZ", self.miniblocks)
        self.gvZ = XYZview(self, "XY", self.miniblocks)
        self.cbSelectBox = QComboBox(self)
        self.pbAddBox = QPushButton("Add Box", self)
        self.pbDeleteBox = QPushButton("Delete selected box", self)
        self.slScale = QSlider(self)
        self.slScale.setOrientation(Qt.Horizontal)
        self.slScale.setRange(5, 15)
        self.pbSwapXY = QPushButton("Spap X and Y", self)
        self.pbSwapXZ = QPushButton("Spap X and Z", self)
        self.pbSwapYZ = QPushButton("Spap Y and Z", self)
        self.pbTurnX  = QPushButton("Turn X", self)
        self.pbTurnY  = QPushButton("Turn Y", self)
        self.pbTurnZ  = QPushButton("Turn Z", self)
        self.grLayout = QGridLayout()
        self.grLayout.addWidget(QLabel("Main view"), 0, 0)
        self.grLayout.addWidget(self.gvMain, 1, 0)
        self.grLayout.addWidget(QLabel("Y view"), 0, 1)
        self.grLayout.addWidget(self.gvY, 1, 1)

        self.vbRightLayout = QVBoxLayout()
        self.vbRightLayout.addWidget(QLabel("Select box"))
        self.vbRightLayout.addWidget(self.cbSelectBox)
        self.vbRightLayout.addWidget(self.pbAddBox)
        self.vbRightLayout.addWidget(self.pbDeleteBox)
        self.vbRightLayout.addWidget(QLabel("Scale"))
        self.vbRightLayout.addWidget(self.slScale)
        self.vbRightLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.vbRightLayout.addWidget(self.pbSwapXY)
        self.vbRightLayout.addWidget(self.pbSwapXZ)
        self.vbRightLayout.addWidget(self.pbSwapYZ)
        self.vbRightLayout.addWidget(self.pbTurnX)
        self.vbRightLayout.addWidget(self.pbTurnY)
        self.vbRightLayout.addWidget(self.pbTurnZ)


        self.hbMainLayout = QHBoxLayout()
        self.hbMainLayout.addLayout(self.grLayout, 10)
        self.hbMainLayout.addLayout(self.vbRightLayout, 1)

        self.grLayout.addWidget(QLabel("X view"), 2, 0)
        self.grLayout.addWidget(self.gvX, 3, 0)
        self.grLayout.addWidget(QLabel("Z view"), 2, 1)
        self.grLayout.addWidget(self.gvZ, 3, 1)
        self.widget.setLayout(self.hbMainLayout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle("CubeMaker")
        self.resize(1000, 600)

    def createMenu(self):
        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu("&File")
        self.helpMenu = self.menuBar.addMenu("&Help")
        self.aNewProject = self.fileMenu.addAction("Start new project")
        self.aOpen = self.fileMenu.addAction("Open")
        self.aSave = self.fileMenu.addAction("Save as...")
        self.aExport = self.fileMenu.addAction("Export as...")
        self.fileMenu.addSeparator()
        self.aExitApp = self.fileMenu.addAction("Exit")
        self.setMenuBar(self.menuBar)

    def addBox(self):
        self.miniblocks.append(MiniBlock(Point(-8, -8, -8),
                                                     Point(8, 8, 8)))
        self.cbSelectBox.addItems(["Block" + str(len(self.miniblocks))])
        self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        self.gvX.update()
        self.gvY.update()
        self.gvZ.update()
        self.current_block = self.miniblocks[self.cbSelectBox.currentIndex()]
        self.gvX.current_block = self.current_block
        self.gvY.current_block = self.current_block
        self.gvZ.current_block = self.current_block

    def deleteBox(self):
        if self.cbSelectBox.count() != 0:
            idx = self.cbSelectBox.currentIndex()
            del self.miniblocks[idx]
            self.cbSelectBox.removeItem(idx)
            try:
                self.cbSelectBox.setCurrentIndex(idx-1)
            except:
                self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        if len(self.miniblocks) == 0:
            self.gvX.current_block = 0
            self.gvY.current_block = 0
            self.gvZ.current_block = 0
        self.update()

    def connectSlots(self):
        self.aExitApp.triggered.connect(lambda: sys.exit(0))
        self.aExport.triggered.connect(self.actionExport)
        self.aSave.triggered.connect(self.actionSave)
        self.aNewProject.triggered.connect(self.actionNewProject)
        self.pbAddBox.clicked.connect(self.addBox)
        self.pbDeleteBox.clicked.connect(self.deleteBox)
        self.cbSelectBox.activated.connect(self.cbSwitch)
        self.slScale.valueChanged.connect(self.slScaleChange)
        self.aOpen.triggered.connect(self.actionOpen)
        self.pbSwapXY.clicked.connect(self.swapXY)
        self.pbSwapXZ.clicked.connect(self.swapXZ)
        self.pbSwapYZ.clicked.connect(self.swapYZ)
        self.pbTurnX.clicked.connect(self.turnX)
        self.pbTurnY.clicked.connect(self.turnY)
        self.pbTurnZ.clicked.connect(self.turnZ)

    def actionNewProject(self):
        self.miniblocks.clear()
        self.current_block = 0
        self.cbSelectBox.clear()
        self.gvX.current_block = 0
        self.gvY.current_block = 0
        self.gvZ.current_block = 0
        self.update()

    def actionExport(self):
        if is_qt5:
            export_as = QFileDialog.getSaveFileName(self, "Export as...")[0]
        else:
            export_as = QFileDialog.getSaveFileName(self, "Export as...")
        create_code = codegen.codegen(self, "mynode", self.miniblocks)
        if export_as != "":
            create_code.writeToFile(export_as)

    def actionSave(self):
        if is_qt5:
            save_as = QFileDialog.getSaveFileName(self, "Save as...")[0]
        else:
            save_as = QFileDialog.getSaveFileName(self, "Save as...")
        if save_as != "":
            output_file = open(save_as, "w+")
            for b in self.miniblocks:
                output_file.write(" ".join([str(b.p1.x), str(b.p1.z), str(b.p1.y),
                                 str(b.p2.x), str(b.p2.z), str(b.p2.y)]) + "\n")
            output_file.close()

    def actionOpen(self):
        if is_qt5:
            open_from = QFileDialog.getOpenFileName(self, "Open file")[0]
        else:
            open_from = QFileDialog.getOpenFileName(self, "Open file")
        input_file = open(open_from, "r")
        self.miniblocks.clear()
        self.gvX.current_block = 0
        self.gvY.current_block = 0
        self.gvZ.current_block = 0
        self.cbSelectBox.clear()
        for line in input_file:
            t = [int(token) for token in line.split(" ")]
            self.miniblocks.append(MiniBlock(Point(t[0], t[2], t[1]), Point(t[3], t[5], t[4])))
            self.cbSelectBox.addItems(["Block" + str(len(self.miniblocks))])
        input_file.close()
        self.update()

    def cbSwitch(self):
        self.current_block = self.miniblocks[self.cbSelectBox.currentIndex()]
        self.gvX.current_block = self.current_block
        self.gvY.current_block = self.current_block
        self.gvZ.current_block = self.current_block

    def slScaleChange(self):
        self.gvX.scale = self.slScale.value()
        self.gvY.scale = self.slScale.value()
        self.gvZ.scale = self.slScale.value()
        self.update()
    
    def swapXY(self):
        for b in self.miniblocks:
            b.p1.x, b.p2.x, b.p1.y, b.p2.y = b.p1.y, b.p2.y, b.p1.x, b.p2.x
        self.update()

    def swapXZ(self):
        for b in self.miniblocks:
            b.p1.x, b.p2.x, b.p1.z, b.p2.z = b.p1.z, b.p2.z, b.p1.x, b.p2.x
        self.update()

    def swapYZ(self):
        for b in self.miniblocks:
            b.p1.y, b.p2.y, b.p1.z, b.p2.z = b.p1.z, b.p2.z, b.p1.y, b.p2.y
        self.update()

    def turnX(self):
        for b in self.miniblocks:
            b.p1.x, b.p2.x = -b.p1.x, -b.p2.x
        self.update()

    def turnY(self):
        for b in self.miniblocks:
            b.p1.y, b.p2.y = -b.p1.y, -b.p2.y
        self.update()

    def turnZ(self):
        for b in self.miniblocks:
            b.p1.z, b.p2.z = -b.p1.z, -b.p2.z
        self.update()

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
