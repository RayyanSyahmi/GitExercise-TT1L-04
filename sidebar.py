import PyQt5 
import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from brush import BrushInput, Brush
import sys
import os

class Sidebar(QtWidgets.QWidget):
    def __init__(self, canvas):
        self.prev_selected_color_button = None
        super().__init__()

        #variables
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)
        
        #layout
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        #colors button
        self.quick_color1 = QPushButton()
        self.quick_color1.setFixedSize(30, 30)
        self.quick_color1.setStyleSheet("background-color: #000000")  # Black
        self.quick_color1.clicked.connect(lambda: self.set_brush_color(0))

        self.quick_color2 = QPushButton()
        self.quick_color2.setFixedSize(30, 30)
        self.quick_color2.setStyleSheet("background-color: #FFFFFF")  # White
        self.quick_color2.clicked.connect(lambda: self.set_brush_color(1))

        self.quick_color3 = QPushButton()
        self.quick_color3.setFixedSize(30, 30)
        self.quick_color3.setStyleSheet("background-color: #007300")  # Green
        self.quick_color3.clicked.connect(lambda: self.set_brush_color(2))

        self.quick_color4 = QPushButton()
        self.quick_color4.setFixedSize(30, 30)
        self.quick_color4.setStyleSheet("background-color: #FFFF00")  # Yellow
        self.quick_color4.clicked.connect(lambda: self.set_brush_color(3))

        #colors layout
        quick_color_layout = QtWidgets.QHBoxLayout()
        quick_color_layout.addWidget(self.quick_color1)
        quick_color_layout.addWidget(self.quick_color2)
        quick_color_layout.addWidget(self.quick_color3)
        quick_color_layout.addWidget(self.quick_color4)
        quick_color_layout.addSpacing(2)
        quick_color_widget = QtWidgets.QWidget()
        quick_color_widget.setLayout(quick_color_layout)

        #size label
        self.brush_size_label = QtWidgets.QLabel("Size: 20")
        #size slider
        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(20)
        size_slider.valueChanged.connect(self.update_slider_label)
        
        #color dialog
        self.color_button = QPushButton('Choose color')
        self.color_button.clicked.connect(lambda: self.open_color_dialog(self.color_button))
    
        #add to sidebar
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(self.color_button)
        layout.addWidget(quick_color_widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(5)

        self.canvas = canvas
        self.canvas_label = QtWidgets.QLabel()
        self.brush = Brush()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)
        self.hide()

        #colors for quick select color
        self.quick_color1_color = "#000000"
        self.quick_color2_color = "#FFFFFF"
        self.quick_color3_color = "#007300"
        self.quick_color4_color = "#FFFF00"

        self.set_brush_color(0)

    def set_brush_color(self, index):
        if index == 0:
            color = self.quick_color1.palette().button().color()
        elif index == 1:
            color = self.quick_color2.palette().button().color()
        elif index == 2:
            color = self.quick_color3.palette().button().color()
        elif index == 3:
            color = self.quick_color4.palette().button().color()

        if color:
            self.brush.color = color
            self.brush.set_color(color)
            self.selected_color = color
        else:
            print("No color selected")

        if index == 0:
            self.prev_selected_color_button = self.quick_color1
        elif index == 1:
            self.prev_selected_color_button = self.quick_color2
        elif index == 2:
            self.prev_selected_color_button = self.quick_color3
        elif index == 3:
            self.prev_selected_color_button = self.quick_color4
    
    def open_color_dialog(self, sender=None):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.brush.color = color
            self.brush.set_color(color)

            if sender == self.color_button:
                if self.prev_selected_color_button:
                    self.prev_selected_color_button.setStyleSheet("background-color: {};".format(color.name()))
                self.prev_selected_color_button = None
            else:
                sender.setStyleSheet("background-color: {};".format(color.name()))
                if sender == self.quick_color1:
                    self.quick_color1_color = color.name()
                elif sender == self.quick_color2:
                    self.quick_color2_color = color.name()
                elif sender == self.quick_color3:
                    self.quick_color3_color = color.name()
                elif sender == self.quick_color4:
                    self.quick_color4_color = color.name()
                self.prev_selected_color_button = sender

    def update_slider_label(self, value):
        self.brush_size_label.setText("Size: {}".format(value))

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
