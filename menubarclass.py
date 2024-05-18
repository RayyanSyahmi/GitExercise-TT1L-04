import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from canvasclass import Canvas
import sys

class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")

        saveAction = QAction("Save", self)
        self.save_action = file_menu.addAction("Save")
        saveAction.triggered.connect(self.save)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    
        if filePath == "":
            return
        self.canvas.save(filePath)