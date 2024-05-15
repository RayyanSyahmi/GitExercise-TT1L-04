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

    def save_file(self):
        types = [("Text Files", "*.txt"),
                 ("All Files", "*.*"),
                 ("Png Files", "*.png"),
                 ("Jpeg Files", "*.jpg *.jpeg")]

        file_path, _ = QFileDialog.getSaveFileName(self,
                                                    "Drawing app saving",
                                                    "",
                                                    "Text Files (*.txt);;Png Files (*.png);;Jpeg Files (*.jpg *.jpeg)",
                                                    options=QFileDialog.DontUseNativeDialog)

        if file_path:
            data = self.entry.text()
            with open(file_path, mode='w') as file_writter:
                file_writter.write(data)
