import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import Brush, Eraser
from sidebar import Sidebar

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brush import Brush, Eraser
from sidebar import Sidebar

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
        self.lines = []
        self.drawing_points = []
        self.last_pos = None
        self.setStyleSheet("background-color: white;")
        self.layers = []
        self.current_layer_index = 0
        self.layers_count = 1
        self.selection_start_pos = None
        self.selecting = False

        self.sidebar = Sidebar(self)  # Initialize sidebar before changing the current layer
        self.sidebar.currentLayerChanged.connect(self.change_current_layer)
        self.change_current_layer(0)
        self.update_canvas()

        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 5
        self.fill_color = self.brush.color  # Initialize fill color with brush color
        self.is_drawing = False
        self.selection_start = None
        self.selection_end = None
        self.is_selecting = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == self.eraser:
                self.save_state()
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
                pen = QPen(self.brush.color, self.brush.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(self.last_pos, event.pos())
                painter.end()
                self.lines.append(pixmap)
        elif event.button() == QtCore.Qt.RightButton:
            self.selecting = True
            self.selection_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            if self.current_tool == self.eraser:
                self.restore_state()
                self.last_pos = event.pos()
                self.drawing_points.append(event.pos())
            else:
                painter = QtGui.QPainter(self.pixmap())
                pen = QtGui.QPen(self.brush.color, self.brush.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
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
                painter.setPen(pen)
                painter.drawLine(self.last_pos, event.pos())
                painter.end()
                self.lines.append(pixmap)
        elif self.selecting:
            # Draw the selection rectangle
            pixmap = QtGui.QPixmap(self.pixmap())
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.DashLine))
            painter.drawRect(QtCore.QRect(self.selection_start_pos, event.pos()))
            painter.end()
            self.setPixmap(pixmap)
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.RightButton and self.selecting:
            self.selecting = False
            self.delete_selection()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        for layer in self.layers:
            canvas_painter.drawPixmap(0, 0, layer)
        if self.selection_start and self.selection_end:
            selection_rect = QRect(self.selection_start, self.selection_end)
            canvas_painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))
            canvas_painter.drawRect(selection_rect)

    def fill_color(self, color):
        self.brush.color = color  # Set brush color to fill color
        self.fill_color = color  # Update fill color
        self.sidebar.update_size_label(color.name())

    def save(self, filePath):
        image = QImage(self.pixmap().size(), QImage.Format_RGB32)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.setBrush(Qt.white)
        painter.drawRect(image.rect())

        for line in self.lines:
            painter.drawPixmap(0, 0, line)

        painter.end()
        image.save(filePath)

    def add_layer(self, index=None):
        layer = QPixmap(1080, 720)
        layer.fill(QtCore.Qt.transparent)
        if index is not None:
            self.layers.insert(index, layer)
            self.layers_count += 1
            self.current_layer_index = index
        else:
            self.layers.append(layer)
            self.layers_count += 1
            self.current_layer_index = self.layers_count - 1
        self.change_current_layer(self.current_layer_index)
        if self.layers_count > 1:
            self.update_canvas()

    def remove_layer(self):
        if self.layers_count > 1:
            if self.current_layer_index < 0 or self.current_layer_index >= self.layers_count:
                self.current_layer_index = 0
            del self.layers[self.current_layer_index]
            self.layers_count -= 1
            self.current_layer_index = min(self.current_layer_index, self.layers_count - 1)

    def change_current_layer(self, index):
        self.sidebar.change_current_layer(index)
        self.current_layer_index = index
        self.update_canvas()

    def clear_layer(self):
        if self.layers_count > 0:
            try:
                self.layers[self.current_layer_index].fill(QtCore.Qt.transparent)
                self.update_canvas()
            except IndexError:
                print(f"Error: Unable to fill layer {self.current_layer_index}. Index is out of range.")
        else:
            print("Error: No layers to clear.")

    def update_canvas(self):
        if self.layers_count > 0 and self.current_layer_index < len(self.layers):
            pixmap = QtGui.QPixmap(1080, 720)
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)

            for layer in self.layers[:self.current_layer_index]:
                painter.setOpacity(0.5)
                painter.drawPixmap(0, 0, layer)

            painter.setOpacity(1.0)
            painter.drawPixmap(0, 0, self.layers[self.current_layer_index])

            painter.end()
            self.setPixmap(pixmap)

    def set_tool(self, tool):
        self.current_tool = tool

    def delete_selection(self):
        if self.selecting:
            self.selecting = False
            start_pos = self.selection_start_pos
            end_pos = self.last_pos
            self.selection_start_pos = None

            rect = QtCore.QRect(min(start_pos.x(), end_pos.x()), min(start_pos.y(), end_pos.y()), abs(end_pos.x() - start_pos.x()), abs(end_pos.y() - start_pos.y()))

            pixmap = self.pixmap()
            painter = QtGui.QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.eraseRect(rect)
            painter.end()

            self.setPixmap(pixmap)
            self.update()

    def fill_selection(self, start, end):
        if start and end:
            selection_rect = QRect(start, end)
            for layer in self.layers:
                painter = QtGui.QPainter(layer)
                painter.setCompositionMode(QPainter.CompositionMode_Source)
                painter.fillRect(selection_rect, self.fill_color)
                painter.end()
            self.update_canvas()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        fill_action = menu.addAction("Fill Selection")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == fill_action:
            self.fill_selection(self.selection_start, self.selection_end)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = Canvas()
    canvas.setWindowTitle("Drawing Application")
    canvas.show()
    sys.exit(app.exec_())

