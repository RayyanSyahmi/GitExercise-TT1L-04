import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import BrushInput, Brush, Eraser, EraserInput
import sys
import os

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

        script_dir = os.path.dirname(os.path.abspath(__file__))

        brushicon = os.path.join(script_dir, 'icons', 'brushicon.png')
        erasericon = os.path.join(script_dir, 'icons', 'erasericon.png')

        self.brush_button = QPushButton()  
        self.brush_button.setFixedHeight(50)
        self.brush_button.setFixedWidth(50)
        self.brush_button.setIcon(QIcon(brushicon))  
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton()
        self.eraser_button.setFixedHeight(50)
        self.eraser_button.setFixedWidth(50)
        self.eraser_button.setIcon(QIcon(erasericon)) 
        self.eraser_button.clicked.connect(self.set_eraser_tool)
        
        self.brush_size_label = QtWidgets.QLabel("Size: 20")

        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(20)
        size_slider.valueChanged.connect(self.update_slider_label)
        
        self.color_button = QPushButton('Choose color')
        self.color_button.clicked.connect(self.open_color_dialog)
        
        layout.addWidget(self.brush_button)  
        layout.addWidget(self.eraser_button)
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(self.color_button)

        layout.setAlignment(Qt.AlignTop)

        self.canvas = canvas
        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        self.eraser_size_input = EraserInput(self.eraser, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)
        self.eraser_button.clicked.connect(self.set_eraser_tool)

        self.hide()

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

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
