import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint 
from PyQt5.QtGui import QColor, QPixmap, QPainter, QPen 
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QSlider, QComboBox, QColorDialog, QHBoxLayout

class Line:
    def __init__(self, point1, point2, brush_size):
        self.point1 = point1
        self.point2 = point2
        self.brush_size = brush_size

class Brush:
    def __init__(self):
        self.size = 5
        self.color = Qt.black
        self.brush = Brush

class Eraser:
    def __init__(self):
        super().__init__()
        self.size = 5

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(1080, 720)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.setStyleSheet("background-color: white;")

        self.lines = []
        self.drawing_points = []

        self.layers = []
        self.current_layer_index = 0
        self.layers_count = 1
        self.layer_opacities = []
        self.current_layer_index = 0

        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)

        self.drawing = False
        self.last_pos = QtCore.QPoint()
        self.drawing_points = []
        self.lines = []

        self.add_layer()

        self.undo_stack = []
        self.redo_stack = []

        self.current_tool = self.Brush  # Set the default tool

        self.update_canvas()

    def save_state(self):
        self.undo_stack.append(self.pixmap().copy())
        self.redo_stack.clear()

    def restore_state(self, pixmap):
        self.setPixmap(pixmap)
        self.update()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.pixmap().copy())
            self.restore_state(self.undo_stack.pop())
            self.update()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.pixmap().copy())
            self.restore_state(self.redo_stack.pop())
            self.update()

    def clearImage(self):
        self.image.fill(Qt.white)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_state()
            if self.current_tool == self.eraser:
                self.last_pos = event.pos()
                self.drawing_points.append(event.pos())
            else:
                self.last_pos = event.pos()
                self.drawing_points.append(event.pos())
                line = Line(self.last_pos, event.pos(), self.brush.size)
                pixmap = QtGui.QPixmap(1080, 720)
                pixmap.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                pen = QPen(Qt.transparent)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)
                brush = QBrush(Qt.white)
                painter.setBrush(brush)
                gradient = QRadialGradient(line.point1, self.brush.size / 2)
                gradient.setColorAt(0, Qt.white)
                gradient.setColorAt(1, Qt.transparent)
                brush = QBrush(gradient)
                painter.setBrush(brush)
                painter.drawEllipse(QRectF(line.point1.x() - self.brush.size / 2, line.point1.y() - self.brush.size / 2, self.brush.size, self.brush.size))
                self.lines.append(pixmap)
        if self.current_tool == self.brush:
            pass
        elif self.current_tool == self.eraser:
            pass
        else:
            pass

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            distance = QtCore.QLineF(self.last_pos, event.pos()).length()
            if distance > self.brush.size / 10000:
                if self.current_tool == self.eraser:
                    self.last_pos = event.pos()
                    self.drawing_points.append(event.pos())
                else:
                    painter = QtGui.QPainter(self.pixmap())
                    pen = QtGui.QPen(QtGui.QPen(self.brush.color, self.brush.size))
                    painter.setPen(pen)
                    painter.drawLine(self.last_pos, event.pos())
                    painter.end()
                    self.update()
                    self.last_pos = event.pos()
                    self.drawing_points.append(event.pos())

                    line = Line(self.last_pos, event.pos(), self.brush.size)
                    pixmap = QtGui.QPixmap(1080, 720)
                    pixmap.fill(QtCore.Qt.transparent)
                    painter = QtGui.QPainter(pixmap)
                    painter.setRenderHint(QPainter.Antialiasing)

                    pen = QPen(Qt.transparent)
                    pen.setJoinStyle(Qt.RoundJoin)
                    painter.setPen(pen)

                    brush = QBrush(self.brush.color)
                    painter.setBrush(brush)

                    gradient = QRadialGradient(line.point1, self.brush.size / 2)
                    gradient.setColorAt(0, self.brush.color)
                    gradient.setColorAt(1, Qt.transparent)
                    brush = QBrush(gradient)
                    painter.setBrush(brush)
                    painter.drawEllipse(QRectF(line.point1.x() - self.brush.size / 2, line.point1.y() - self.brush.size / 2, self.brush.size, self.brush.size))

                    self.lines.append(pixmap)

                    color = self.get_pixel_color(self.x(), self.y())
                    self.parent().statusBar().showMessage(f"Pixel color: {color.name()}")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = None

    def update_brush_size(self, new_size):
        self.brush.size = new_size

    def update_brush_color(self, new_color):
        self.brush.color = new_color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())
        painter.drawPixmap(0, 0, self.pixmap())
            
    def color_pickout(self, color):
        print ("pick")
        painter = QtGui.QPainter(self.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(color)
        brush.setStyle(Qt.SolidPattern)

    def save(self, filePath):
        self.pixmap().save(filePath)

    def add_layer(self, index=None):
        new_layer = QPixmap(self.size())
        new_layer.fill(Qt.transparent)
        if index is not None:
            self.layers.insert(index, new_layer)
            self.layers_count += 1
            self.current_layer_index = index
        else:
            self.layers.append(new_layer)
            self.layers_count += 1
            self.current_layer_index = self.layers_count - 1
        self.change_current_layer(self.current_layer_index)
        if self.layers_count > 1:
            self.update_canvas()

    def remove_layer(self):
        if self.layers_count > 1:
            if self.current_layer_index < 0 or self.current_layer_index >= self.layers_count:
                self.current_layer_index = 0
            print(f"Removing layer at index {self.current_layer_index}")
            del self.layers[self.current_layer_index]
            self.layers_count -= 1
            self.current_layer_index = min(self.current_layer_index, self.layers_count - 1)

    def change_current_layer(self, index):
        self.current_layer_index = index
        self.update_canvas()

    def clear_layer(self):
        if self.layers_count > 0:
            try:
                self.layers[self.current_layer_index - 1].fill(Qt.transparent)
                self.update_canvas()
            except IndexError:
                print(f"Error: Unable to fill layer {self.current_layer_index}. Index is out of range.")
        else:
            print("Error: No layers to clear.")

    def update_canvas(self):
        if self.layers_count > 0 and self.current_layer_index < len(self.layers):
            pixmap = QPixmap(1080, 720)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            for layer in self.layers[:self.current_layer_index]:
                painter.setOpacity(0.5)
                painter.drawPixmap(0, 0, layer)
            painter.setOpacity(1.0)
            painter.drawPixmap(0, 0, self.layers[self.current_layer_index])
            painter.end()
            self.setPixmap(pixmap)

    def set_tool(self, tool):
        print("Setting tool to", tool)
        self.current_tool = tool
