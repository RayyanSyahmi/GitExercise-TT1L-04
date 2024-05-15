import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Brush:
    def __init__(self, size=20, color=Qt.black):
        self.size = size
        self.color = color
        self.shape = "circle"

    def set_color(self, color):
        self.color = color

    def set_size(self, size):
        self.size = size

class Eraser():
    def __init__(self, eraser_size=20, eraser_color=Qt.white):
        self.eraser_size = eraser_size
        self.eraser_color = eraser_color

class BrushInput(QtWidgets.QWidget):
    def __init__(self, brush, canvas):
        super().__init__()
        self.canvas = canvas
        self.brush = brush
        self.brush_size_input = QtWidgets.QLineEdit(self)
        self.brush_size_input.setPlaceholderText("Brush size")
        self.brush_size_input.setGeometry(10, 10, 80, 20)
        self.brush_size_input.returnPressed.connect(self.set_brush_radius_from_input)

        self.color_button = QtWidgets.QPushButton("Choose color", self)
        self.color_button.clicked.connect(self.choose_color)
        self.canvas.brush = self.brush

    @pyqtSlot(int)
    def update_brush_size(self, new_size):
        self.brush_size_input.setText(str(new_size))
        self.brush.set_size(new_size)
        self.canvas.brush.size = new_size
        self.canvas.brush.shape = "circle"
        
    def set_brush_radius_from_input(self):
        try:
            self.brush.size = int(self.brush_size_input.text())
            self.brush.set_size(self.brush.size)
            self.brush_size_input.clear()
        except ValueError:
            pass

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush.color = color
            self.brush.set_color(color)
            self.canvas.brush.color = color

