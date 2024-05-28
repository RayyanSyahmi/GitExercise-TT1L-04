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
        self.lines = []
        self.drawing_points = []
        self.last_pos = None
        self.setStyleSheet("background-color: white;")

    def set_tool(self, tool):
        self.current_tool = tool

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
                    self.restore_state()
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


    def update_brush_size(self, new_size):
        self.brush.size = new_size

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill the canvas with a white background
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())

        for line in self.lines:
            painter.drawPixmap(0, 0, line)

    def save(self, filePath):
        image = QImage(self.pixmap().size(), QImage.Format_RGB32)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Fill the image with a white background
        painter.setBrush(Qt.white)
        painter.drawRect(image.rect())

        for line in self.lines:
            painter.drawPixmap(0, 0, line)

        painter.end()
        image.save(filePath)
    
    def set_tool(self, tool):
        print("Setting tool to", tool)
        self.current_tool = tool