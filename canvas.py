import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint 
from PyQt5.QtGui import QColor, QPixmap, QPainter, QPen 
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QSlider, QComboBox, QColorDialog, QHBoxLayout
from brush import Brush, Eraser

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(1080, 720)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.brush = Brush()
        self.eraser = Eraser()
        self.setStyleSheet("background-color: white;")

        self.lines = []
        self.drawing_points = []

        self.layers = []
        self.current_layer_index = 0
        self.layers_count = 1
        self.layer_opacities = []
        self.current_layer_index = 0

        self.add_layer()

        self.undo_stack = []
        self.redo_stack = []

        self.current_tool = self.brush  # Set the default tool

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

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.pixmap().copy())
            self.restore_state(self.redo_stack.pop())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_state()
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_pos:
            painter = QPainter(self.pixmap())
            if self.current_tool == self.eraser:
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
                pen = QPen(Qt.transparent, self.eraser.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            else:
                pen = QPen(self.brush.color, self.brush.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())

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
