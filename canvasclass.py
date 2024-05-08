import sys
import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import Brush


class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QtGui.QPixmap(1080, 720))
        pixmap = QtGui.QPixmap(1080, 720)
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.end()
        self.setPixmap(pixmap)
        self.update()
        self.brush = Brush()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            painter = QtGui.QPainter(self.pixmap())
            pen = QtGui.QPen(QtGui.QPen(self.brush.color, self.brush.size))
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()

    def update_brush_size(self, new_size):
        self.brush_size_input.update_brush_size(new_size)

