<<<<<<< HEAD
import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from canvasclass import Canvas
from canvas import Canvas
import sys
import os

class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.save)
        self.save_action = file_menu.addAction(saveAction)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')

        undo_action = QAction(QIcon(undoicon), 'Undo', self)
        redo_action = QAction(QIcon(redoicon), 'Redo', self)

        self.addAction(undo_action)
        self.addAction(redo_action)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    
        if filePath == "":
            return
=======
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
        saveAction.triggered.connect(self.save)
        self.save_action = file_menu.addAction(saveAction)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    
        if filePath == "":
            return
>>>>>>> 5af4395bd3dfeb877c677fe2f9eb3babe5054877
        self.canvas.save(filePath)