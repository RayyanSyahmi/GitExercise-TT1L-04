import PyQt5 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Brush:
    def __init__(self, size=2, color=Qt.black, brush_radius=5, brush_offset=QPoint(0, 0)):
        self.size = size
        self.color = color
        self.brush_radius = brush_radius
        self.brush_offset = brush_offset