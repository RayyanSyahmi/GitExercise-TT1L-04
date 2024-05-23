import sys
import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import Brush, Eraser

class Line:
    def __init__(self, point1, point2, brush_size):
        self.point1 = point1
        self.point2 = point2
        self.brush_size = brush_size

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
        self.eraser = Eraser()
        self.current_tool = None
        self.drawing_points = []
        self.setStyleSheet("background-color: white;")

        self.add_layer()
    
    def set_tool(self, tool):
        self.current_tool = tool

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            painter = QtGui.QPainter(self.pixmap())
            pen = QtGui.QPen(QtGui.QPen(self.brush.color, self.brush.size))
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())

    def update_brush_size(self, new_size):
        self.brush.size = new_size

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.transparent)  
        pen.setJoinStyle(Qt.RoundJoin)  
        painter.setPen(pen)

        brush = QBrush(self.brush.color)
        painter.setBrush(brush)

        for point in self.drawing_points:
            gradient = QRadialGradient(point, self.brush.size / 2)
            gradient.setColorAt(0, self.brush.color)
            gradient.setColorAt(1, Qt.transparent)
            brush = QBrush(gradient)
            painter.setBrush(brush)
            painter.drawEllipse(QRectF(point.x() - self.brush.size / 2, point.y() - self.brush.size / 2, self.brush.size, self.brush.size))

    def save(self, filePath):
        pixmap = self.pixmap()
        pixmap.save(filePath) 

    def add_layer(self):
        layer_index = len(self.layers)
        layer = QImage(1200, 900, QImage.Format_ARGB32)
        layer.fill(Qt.transparent)
        self.layers.append(layer)
        
        self.layer_combo_box.addItem(f"Layer {layer_index + 1}")
        self.layer_combo_box.setCurrentIndex(layer_index)

    def remove_layer(self):
        if len(self.layers) > 1:
            self.layers.pop()
            self.layer_combo_box.removeItem(len(self.layers))
            self.current_layer_index = min(self.current_layer_index, len(self.layers) - 1)

    def clear_layer(self):
        if self.current_layer_index < len(self.layers):
            self.layers[self.current_layer_index].fill(Qt.transparent)
        self.update_canvas()

    def change_current_layer(self, index):
        self.current_layer_index = index
        self.update_canvas()

    def draw_point(self, pos):
        painter = QPainter(self.layers[self.current_layer_index])
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPoint(pos)

    def update_canvas(self):
        self.canvas_pixmap = QPixmap(1200, 900)
        self.canvas_pixmap.fill(Qt.white)
        painter = QPainter(self.canvas_pixmap)
        painter.drawImage(0, 0, self.layers[self.current_layer_index])
        for i, layer in enumerate(self.layers[:self.current_layer_index]):
            painter.setOpacity(0.5)
            painter.drawImage(0, 0, layer)
        painter.end()
        self.canvas_label.setPixmap(self.canvas_pixmap)
