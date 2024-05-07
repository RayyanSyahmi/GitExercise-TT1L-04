import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brushes import BrushSizeInput, Brush
from canvasclass import Canvas
import sys

class Sidebar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        self.setLayout(layout)

        self.brush_size_label = QtWidgets.QLabel("Size: 5")
        layout.addWidget(self.brush_size_label)

        self.brush_settings_widget = QtWidgets.QWidget()
        brush_settings_layout = QtWidgets.QVBoxLayout()
        brush_settings_layout.setSpacing(0)
        self.brush_settings_widget.setLayout(brush_settings_layout)

        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(self.update_slider_label)
        brush_settings_layout.addWidget(size_slider)

        self.color_button = QtWidgets.QPushButton("Choose color", self)
        self.color_button.clicked.connect(self.open_color_dialog)
        brush_settings_layout.addWidget(self.color_button)

        self.brush = Brush()
        self.brush_size_input = BrushSizeInput(self.brush)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)

        layout.addWidget(self.brush_settings_widget)

        layout.addStretch(1)

    def update_slider_label(self, value):
        self.brush_size_label.setText("Size: {}".format(value))

    def open_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush.color = color
            self.brush.set_color(color)