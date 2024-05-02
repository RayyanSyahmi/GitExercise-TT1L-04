import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Brush:
    def __init__(self, size = 2, color=Qt.black):
        self.size = size
        self.color = color

    def set_size(self, size):
        self.size = size
        self.brush_radius = size

class BrushSizeInput(QtWidgets.QWidget):
    def __init__(self, brush, parent=None):
        super().__init__(parent)
        self.brush = brush
        self.brush_size_input = QtWidgets.QLineEdit(self)
        self.brush_size_input.setPlaceholderText("Brush size")
        self.brush_size_input.setGeometry(10, 10, 80, 20)
        self.brush_size_input.returnPressed.connect(self.set_brush_radius_from_input)

    @pyqtSlot(int)
    def update_brush_size(self, new_size):
        print(f"Brush size updated to: {new_size}")  # Add this print statement
        self.brush_size_input.setText(str(new_size))
        self.brush.set_size(new_size)
        print(f"Brush size: {self.brush.size}")  # Add this print statement

    def set_brush_radius_from_input(self):
        try:
            self.brush.size = int(self.brush_size_input.text())
            self.brush.set_size(self.brush.size)
            self.brush_size_input.clear()
        except ValueError:
            pass

