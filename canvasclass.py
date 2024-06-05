import sys
import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brushes import Brush, BrushSizeInput

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(1080, 720)
        self.pixmap.fill(Qt.white)
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.pixmap)
        self.setScene(self.scene)
        self.setFixedSize(1080, 720)
        self.last_pos = None
        self.brush = Brush(Qt.black, 5)
        
    def update_brush_size(self, text):
        try:
            self.brush.size = int(text)
            self.brush.set_size(self.brush.size)
        except ValueError:
            pass

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

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.MouseMove:
            print("Mouse move event received")
        return super().eventFilter(obj, event)