#!/usr/bin/env python3

from PyQt5.QtWidgets import (QPushButton, QGridLayout, QWidget, QApplication,
                             QLabel, QMenuBar, QVBoxLayout,
                             QHBoxLayout, QMainWindow, QFileDialog, QComboBox,
                             QSpacerItem, QSizePolicy, QSlider)
import sys
import newproject
import codegen
from xyzview import XYZview
from mainview import MainView
from point import MiniBlock, Point
from PyQt5.QtCore import Qt


class Data():
    def __init__(self):
        self.parts = []
        self.MiniBlocks = []
        self.centralBlock = Point(0, 0, 0)

    def setPart(self, x, y):
        self.parts.append([x, y])

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.projectData = Data()
        self.createGUI()
        self.createMenu()
        self.connectSlots()
        self.project_file = ""
        self.current_block = 0

    def createGUI(self):
        self.widget = QWidget(self)
        self.gvMain = MainView(self)
        self.gvX = XYZview(self, "YZ", self.projectData.MiniBlocks)
        self.gvY = XYZview(self, "XZ", self.projectData.MiniBlocks)
        self.gvZ = XYZview(self, "XY", self.projectData.MiniBlocks)
        self.cbSelectBox = QComboBox(self)
        self.pbAddBox = QPushButton("Add Box", self)
        self.pbDeleteBox = QPushButton("Delete selected box", self)
        self.slScale = QSlider(self)
        self.slScale.setOrientation(Qt.Horizontal)
        self.slScale.setRange(5, 15)
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

        self.hbMainLayout = QHBoxLayout()
        self.hbMainLayout.addLayout(self.grLayout, 10)
        self.hbMainLayout.addLayout(self.vbRightLayout, 1)

        self.grLayout.addWidget(QLabel("X view"), 2, 0)
        self.grLayout.addWidget(self.gvX, 3, 0)
        self.grLayout.addWidget(self.gvZ, 3, 1)
        self.grLayout.addWidget(QLabel("Z view"), 2, 1)
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
        self.aOpen = self.fileMenu.addAction("Save as...")
        self.aExport = self.fileMenu.addAction("Export as...")
        self.fileMenu.addSeparator()
        self.aExitApp = self.fileMenu.addAction("Exit")
        self.setMenuBar(self.menuBar)

    def addBox(self):
        self.projectData.MiniBlocks.append(MiniBlock(Point(-1, -1, -1),
                                                     Point(8, 8, 8)))
        self.cbSelectBox.addItems(["Block" + str(len(self.projectData.MiniBlocks))])
        self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        self.gvX.update()
        self.gvY.update()
        self.gvZ.update()
        self.current_block = self.projectData.MiniBlocks[self.cbSelectBox.currentIndex()]
        self.gvX.current_block = self.current_block
        self.gvY.current_block = self.current_block
        self.gvZ.current_block = self.current_block

    def deleteBox(self):
        if self.cbSelectBox.count() != 0:
            idx = self.cbSelectBox.currentIndex()
            del self.projectData.MiniBlocks[idx]
            self.cbSelectBox.removeItem(idx)
            try:
                self.cbSelectBox.setCurrentIndex(idx-1)
            except:
                self.cbSelectBox.setCurrentIndex(self.cbSelectBox.count()-1)
        self.gvX.update()
        self.gvY.update()
        self.gvZ.update()

    def connectSlots(self):
        self.aExitApp.triggered.connect(lambda: sys.exit(0))
        self.aExport.triggered.connect(self.actionExport)
        self.aNewProject.triggered.connect(self.actionNewProject)
        self.pbAddBox.clicked.connect(self.addBox)
        self.pbDeleteBox.clicked.connect(self.deleteBox)
        self.cbSelectBox.activated.connect(self.cbSwitch)
        self.slScale.valueChanged.connect(self.slScaleChange)

    def actionNewProject(self):
        a = newproject.NewProjectDialog(self)
        a.raise_()
        a.exec_()

    def actionExport(self):
        export_as = QFileDialog.getSaveFileName(self, "Export as...")
        create_code = codegen.codegen(self, "mynode", self.projectData.MiniBlocks)
        if export_as != "":
            create_code.writeToFile(export_as[0])

    def cbSwitch(self):
        self.current_block = self.projectData.MiniBlocks[self.cbSelectBox.currentIndex()]
        self.gvX.current_block = self.current_block
        self.gvY.current_block = self.current_block
        self.gvZ.current_block = self.current_block

    def slScaleChange(self):
        self.gvX.scale = self.slScale.value()
        self.gvY.scale = self.slScale.value()
        self.gvZ.scale = self.slScale.value()
        self.update()


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
