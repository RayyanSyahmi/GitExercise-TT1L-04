import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys



class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super().__init__()

        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        self.save_action = file_menu.addAction("Save")
        self.save_action.triggered.connect(self.save_file)
        file_menu.addAction("Exit")

    def save_file():
        types = [ ("Image Files", "*.png"),
                ("All Files", "*.*")]

        file_path = QFileDialog.getSaveFileName(title = "Custom Save Title",
                                            filter = ";;".join(f"{name} ({pattern})" for name, pattern in types),
                                            initialdir=".")

        if file_path != "":
            pixmap = self.canvas.grab()
            pixmap.save(file_path)
