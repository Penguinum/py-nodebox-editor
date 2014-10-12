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
from point import MiniBlock


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.parts = []
        self.miniblocks = []
        self.centralBlock = [0, 0, 0, 1]
        self.resolution = 16
        self.createGUI()
        self.createMenu()
        self.connectSlots()
        self.project_file = ""
        self.current_block = 0
        self.block_count = 0


    def createGUI(self):
        self.widget = QWidget(self)
        self.gvMain = MainView(self, 0, self.miniblocks)
        self.gvX = XYZview(self, "YZ", self.miniblocks)
        self.gvY = XYZview(self, "XZ", self.miniblocks)
        self.gvZ = XYZview(self, "XY", self.miniblocks)
        self.cbSelectBox = QComboBox(self)
        self.pbAddBox = QPushButton("Add Box", self)
        self.pbDeleteBox = QPushButton("Delete selected box", self)
        self.slScale = QSlider(self)
        self.slScale.setOrientation(Qt.Horizontal)
        self.slScale.setRange(2, 15)
        self.slScale.setValue(5)
        self.pbSwapXY = QPushButton("Swap X and Y", self)
        self.pbSwapXZ = QPushButton("Swap X and Z", self)
        self.pbSwapYZ = QPushButton("Swap Y and Z", self)
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
        self.miniblocks.append(MiniBlock([-8, -8, -8, 1],
                                                     [8, 8, 8, 1]))
        self.block_count += 1 # BTW, we will not decrease this value
        self.cbSelectBox.addItems(["Block" + str(self.block_count)])
        self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        self.update()
        self.current_block = self.miniblocks[self.cbSelectBox.currentIndex()]
        self.sendCurrentBlock(self.current_block)

    def deleteBox(self):
        if self.cbSelectBox.count() != 0:
            idx = self.cbSelectBox.currentIndex()
            del self.miniblocks[idx]
            self.cbSelectBox.removeItem(idx)
            if self.cbSelectBox.count() != 0:
                self.cbSelectBox.setCurrentIndex(0)
                self.current_block = self.miniblocks[0]
                self.sendCurrentBlock(self.current_block)
            else:
                self.current_block = 0;
                self.sendCurrentBlock(0)
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
        self.sendCurrentBlock(0)
        self.block_count = 0
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
                output_file.write(" ".join([str(b.p1()[0]), str(b.p1()[2]), str(b.p1()[1]),
                                 str(b.p2()[0]), str(b.p2()[2]), str(b.p2()[1])]) + "\n")
            output_file.close()

    def sendCurrentBlock(self, block):
        self.gvX.current_block =    block
        self.gvY.current_block =    block
        self.gvZ.current_block =    block
        #self.gvMain.current_block = block

    def sendScale(self, scale):
        self.gvX.scale    = scale
        self.gvY.scale    = scale
        self.gvZ.scale    = scale
        self.gvMain.scale = scale

    def sendResolution(self, resolution):
        self.gvX.resolution    = resolution
        self.gvY.resolution    = resolution
        self.gvZ.resolution    = resolution
        self.gvMain.resolution = resolution

    def actionOpen(self):
        if is_qt5:
            open_from = QFileDialog.getOpenFileName(self, "Open file")[0]
        else:
            open_from = QFileDialog.getOpenFileName(self, "Open file")
        input_file = open(open_from, "r")
        self.miniblocks.clear()
        self.sendCurrentBlock(0)
        self.cbSelectBox.clear()
        for line in input_file:
            t = [int(token) for token in line.split(" ")]
            self.miniblocks.append(MiniBlock([t[0], t[2], t[1], 1], [t[3], t[5], t[4], 1]))
            self.cbSelectBox.addItems(["Block" + str(len(self.miniblocks))])
        input_file.close()
        self.update()

    def cbSwitch(self):
        self.current_block = self.miniblocks[self.cbSelectBox.currentIndex()]
        self.sendCurrentBlock(self.current_block)
        self.update()

    def slScaleChange(self):
        self.sendScale(self.slScale.value())
        self.update()

    def swapXY(self):
        for b in self.miniblocks:
            b.swapXY()
        self.update()

    def swapXZ(self):
        for b in self.miniblocks:
            b.swapXZ()
        self.update()

    def swapYZ(self):
        for b in self.miniblocks:
            b.swapYZ()
        self.update()

    def turnX(self):
        for b in self.miniblocks:
            b.turnX()
        self.update()

    def turnY(self):
        for b in self.miniblocks:
            b.turnY()
        self.update()

    def turnZ(self):
        for b in self.miniblocks:
            b.turnZ()
        self.update()

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
