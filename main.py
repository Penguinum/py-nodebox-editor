#!/usr/bin/env python3

try:
    from PyQt5.QtWidgets import (QPushButton, QGridLayout,
        QWidget, QApplication, QLabel, QMenuBar, QVBoxLayout,
        QHBoxLayout, QMainWindow, QFileDialog, QComboBox,
        QSpacerItem, QSizePolicy, QSlider)
    from PyQt5.QtCore import Qt
    using_qt5 = True
except:
    from PyQt4.QtGui import (QPushButton, QGridLayout,
        QWidget, QApplication, QLabel, QMenuBar, QVBoxLayout,
        QHBoxLayout, QMainWindow, QFileDialog, QComboBox,
        QSpacerItem, QSizePolicy, QSlider)
    from PyQt4.QtCore import Qt
    using_qt5 = False

import sys
import codegen
from xyzview import *
from mainview import MainView
from block import Block
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.parts = []
        self.blocks = []
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
        self.gvMain = MainView(self, 0, self.blocks)
        self.views = {key: XYZview(self, self.blocks, key)
                for key in ('xy', 'yz', 'zx')}
        self.cbSelectBox = QComboBox(self)
        self.pbAddBox = QPushButton("Add Box", self)
        self.pbDeleteBox = QPushButton("Delete selected box", self)
        self.slScale = QSlider(self)
        self.slScale.setOrientation(Qt.Horizontal)
        self.slScale.setRange(2, 15)
        self.slScale.setValue(5)
        self.slResolution = QSlider(self)
        self.slResolution.setOrientation(Qt.Horizontal)
        self.slResolution.setRange(1, 6) # resolution is 2**this_value
        self.slResolution.setValue(4) # 2**4 is 16 -- initial resolution
        self.turn_buttons = {'x': QPushButton("Turn around X axis", self),
                             'y': QPushButton("Turn around Y axis", self),
                             'z': QPushButton("Turn around Z axis", self)}
        self.swap_buttons = {'xy': QPushButton("Swap X and Y", self),
                             'yz': QPushButton("Swap Y and Z", self),
                             'zx': QPushButton("Swap Z and X", self)}
        self.grLayout = QGridLayout()
        self.grLayout.addWidget(QLabel("Main view"), 0, 0)
        self.grLayout.addWidget(self.gvMain, 1, 0)
        self.grLayout.addWidget(QLabel("Y view"), 0, 1)
        self.grLayout.addWidget(self.views['zx'], 1, 1)

        self.vbRightLayout = QVBoxLayout()
        self.vbRightLayout.addWidget(QLabel("Select box"))
        self.vbRightLayout.addWidget(self.cbSelectBox)
        self.vbRightLayout.addWidget(self.pbAddBox)
        self.vbRightLayout.addWidget(self.pbDeleteBox)
        self.vbRightLayout.addWidget(QLabel("Scale"))
        self.vbRightLayout.addWidget(self.slScale)
        self.vbRightLayout.addWidget(QLabel("Resolution"))
        self.vbRightLayout.addWidget(self.slResolution)
        self.vbRightLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        for button in self.swap_buttons.values():
            self.vbRightLayout.addWidget(button)
        for button in self.turn_buttons.values():
            self.vbRightLayout.addWidget(button)

        self.hbMainLayout = QHBoxLayout()
        self.hbMainLayout.addLayout(self.grLayout, 10)
        self.hbMainLayout.addLayout(self.vbRightLayout, 1)

        self.grLayout.addWidget(QLabel("X view"), 2, 0)
        self.grLayout.addWidget(self.views['yz'], 3, 0)
        self.grLayout.addWidget(QLabel("Z view"), 2, 1)
        self.grLayout.addWidget(self.views['xy'], 3, 1)
        self.widget.setLayout(self.hbMainLayout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle("Nodebox editor")
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
        self.blocks.append(Block([-8, -8, -8, 1],
                                 [8, 8, 8, 1]))
        self.block_count += 1 # BTW, we will not decrease this value
        self.cbSelectBox.addItems(["Block" + str(self.block_count)])
        self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        self.update()
        self.current_block = self.blocks[self.cbSelectBox.currentIndex()]
        self.sendCurrentBlock(self.current_block)

    def deleteBox(self):
        if self.cbSelectBox.count() != 0:
            idx = self.cbSelectBox.currentIndex()
            del self.blocks[idx]
            self.cbSelectBox.removeItem(idx)
            if self.cbSelectBox.count() != 0:
                self.cbSelectBox.setCurrentIndex(0)
                self.current_block = self.blocks[0]
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
        self.slResolution.valueChanged.connect(self.slResolutionChange)
        self.aOpen.triggered.connect(self.actionOpen)
        for (key, button) in self.turn_buttons.items():
            button.clicked.connect(partial(self.turn, key))
        for (key, button) in self.swap_buttons.items():
            button.clicked.connect(partial(self.swap, key))

    def actionNewProject(self):
        self.blocks.clear()
        self.current_block = 0
        self.cbSelectBox.clear()
        self.sendCurrentBlock(0)
        self.block_count = 0
        self.update()

    def actionExport(self):
        if using_qt5:
            export_as = QFileDialog.getSaveFileName(self, "Export as...")[0]
        else:
            export_as = QFileDialog.getSaveFileName(self, "Export as...")
        create_code = codegen.codegen(self, "mynode", self.blocks, self.resolution)
        if export_as != "":
            create_code.writeToFile(export_as)

    def actionSave(self):
        if using_qt5:
            save_as = QFileDialog.getSaveFileName(self, "Save as...")[0]
        else:
            save_as = QFileDialog.getSaveFileName(self, "Save as...")
        if save_as != "":
            output_file = open(save_as, "w+")
            for b in self.blocks:
                output_file.write(" ".join([
                    str(b.p1()[0]), str(b.p1()[2]), str(b.p1()[1]),
                    str(b.p2()[0]), str(b.p2()[2]), str(b.p2()[1])]) + "\n")
            output_file.close()

    def sendCurrentBlock(self, block):
        for view in self.views.values():
            view.set_current_block(block)

    def sendScale(self, scale):
        for view in self.views.values():
            view.set_scale(scale)
        self.gvMain.scale = scale

    def sendResolution(self, resolution):
        for view in self.views.values():
            view.set_resolution(resolution)
        self.gvMain.resolution = resolution
        self.resolution        = resolution

    def actionOpen(self):
        if using_qt5:
            open_from = QFileDialog.getOpenFileName(self, "Open file")[0]
        else:
            open_from = QFileDialog.getOpenFileName(self, "Open file")
        input_file = open(open_from, "r")
        self.blocks.clear()
        self.sendCurrentBlock(0)
        self.cbSelectBox.clear()
        for line in input_file:
            t = [int(token) for token in line.split(" ")]
            self.blocks.append(Block([t[0], t[2], t[1], 1],
                [t[3], t[5], t[4], 1]))
            self.cbSelectBox.addItems(["Block" + str(len(self.blocks))])
        input_file.close()
        self.update()

    def cbSwitch(self):
        self.current_block = self.blocks[self.cbSelectBox.currentIndex()]
        self.sendCurrentBlock(self.current_block)
        self.update()

    def slScaleChange(self):
        self.sendScale(self.slScale.value())
        self.update()

    def slResolutionChange(self):
        self.sendResolution(2**self.slResolution.value())
        self.update()

    def swap(self, coords):
        for b in self.blocks:
            b.swap(coords)
        self.update()

    def turn(self, coord):
        for b in self.blocks:
            b.turn(coord)
        self.update()


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

