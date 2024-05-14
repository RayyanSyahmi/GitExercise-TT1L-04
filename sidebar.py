import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import BrushInput, Brush, Eraser
import sys

class Sidebar(QtWidgets.QWidget):
    def __init__(self, canvas):
        super().__init__()

        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        self.brush_button = QPushButton('Brush')  
        self.brush_button.setToolTip('Select The Brush tool')
        self.brush_button.setFixedHeight(30)
        self.brush_button.setFixedWidth(80)
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton('Eraser')
        self.eraser_button.setToolTip('Select The Eraser Tool')  # Adding tooltip here
        self.eraser_button.setFixedHeight(30)
        self.eraser_button.setFixedWidth(80)
        self.eraser_button.clicked.connect(self.set_eraser_tool)
        
        self.brush_size_label = QtWidgets.QLabel("Size: 20")

        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(20)
        size_slider.valueChanged.connect(self.update_slider_label)
        

        layout.addWidget(self.brush_button)  
        layout.addWidget(self.eraser_button)
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(QtWidgets.QPushButton("Choose color", self))

        layout.setAlignment(Qt.AlignTop)

        self.canvas = canvas
        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)

    def update_slider_label(self, value):
        self.brush_size_label.setText("Size: {}".format(value))

    def open_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush.color = color
            self.brush.set_color(color)

    def set_brush_tool(self):
        self.active_tool = "Brush"
        self.brush_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.brush)

    def set_eraser_tool(self):
        self.active_tool = "Eraser"
        self.eraser_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.eraser)