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
      
        layout.addWidget(self.brush_button)  
        layout.addWidget(self.eraser_button)

        layout.setAlignment(self.brush_button, Qt.AlignTop)
        layout.setAlignment(self.eraser_button, Qt.AlignTop)

        self.canvas = canvas
        self.tool = Brush()

    def set_brush_tool(self):
        self.active_tool = "Brush"
        self.brush_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.tool = Brush()
        self.canvas.set_tool(self.tool)

    def set_eraser_tool(self):
        self.active_tool = "Eraser"
        self.eraser_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.tool = Eraser(eraser_size=20, eraser_color=Qt.white)
        self.canvas.set_tool(self.tool)