import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Brush:
    def __init__(self, size=20, color=None):
        self.size = size
        self.color = color if color else QtGui.QColor("black")
        self.canvas = None

    def set_canvas(self, canvas):
        self.canvas = canvas 

    def set_color(self, color):
        print(f"Brush color changed to: {color}")
        self.color = color
        if self.canvas: 
            self.canvas.brush.color = color

    def set_size(self, new_size):
        self.size = new_size
        
class Eraser:
    def __init__(self, eraser_size=20, eraser_color=Qt.white):
        self.size = eraser_size
        self.color = eraser_color
        self.shape = "square"

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

class BrushInput(QtWidgets.QWidget):
    def __init__(self, brush, canvas):
        super().__init__()
        self.canvas = canvas
        self.brush = brush
        self.brush_size_input = QtWidgets.QLineEdit(self)

        self.brush_size_input.returnPressed.connect(self.set_brush_radius_from_input)

        self.color_button = QtWidgets.QPushButton("Choose color", self)
        self.color_button.clicked.connect(self.choose_color)
        self.canvas.brush = self.brush

    @pyqtSlot(int)
    def update_brush_size(self, new_size):
        self.brush_size_input.setText(str(new_size))
        self.brush.set_size(new_size)
        self.canvas.brush.size = new_size


    def set_brush_radius_from_input(self):
        try:
            if self.brush_size_input.text():
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

class EraserInput(QtWidgets.QWidget):
    def __init__(self, eraser, canvas):
        super().__init__()
        self.canvas = canvas
        self.eraser = eraser
        self.eraser_size_input = QtWidgets.QLineEdit(self)
        self.eraser_size_input.setPlaceholderText("Eraser size")
        self.eraser_size_input.setGeometry(10, 10, 80, 20)
        self.eraser_size_input.returnPressed.connect(self.set_eraser_size_from_input)

        self.canvas.eraser = self.eraser

    @pyqtSlot(int)
    def update_eraser_size(self, new_size):
        self.eraser_size_input.setText(str(new_size))
        self.eraser.set_size(new_size)
        self.canvas.eraser.size = new_size

    def set_eraser_size_from_input(self):
        try:
            if self.eraser_size_input.text():
                self.eraser.size = int(self.eraser_size_input.text())
                self.eraser.set_size(self.eraser.size)
                self.canvas.eraser.size = self.eraser.size
                self.eraser_size_input.clear()
        except ValueError:
            pass