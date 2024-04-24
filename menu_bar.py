import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class BrushSizeInput(QtWidgets.QWidget):
    def __init__(self, brush, parent=None):
        super().__init__(parent)
        self.brush = brush
        self.brush_size_input = QtWidgets.QLineEdit(self)
        self.brush_size_input.setPlaceholderText("Brush size")
        self.brush_size_input.setGeometry(10, 10, 80, 20)
        self.brush_size_input.returnPressed.connect(self.set_brush_radius_from_input)

    def set_brush_radius_from_input(self):
        try:
            self.brush.size = int(self.brush_size_input.text())
            self.brush.set_size(self.brush.size)
            self.brush_size_input.clear()
        except ValueError:
            pass