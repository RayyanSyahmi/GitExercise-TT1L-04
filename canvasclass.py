import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QLabel
from brush import Brush, Eraser

class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QPixmap(1080, 720))
        pixmap = QPixmap(1080, 720)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.brush = Brush()
        self.eraser = Eraser()
        self.current_tool = None
        self.drawing_points = []
        self.selection_rect = QRect()
        self.selection_start = None
        self.selection_end = None
        self.dragging_selection = False
        self.resizing_selection = False
        self.resize_direction = None
        self.setStyleSheet("background-color: white;")

    def set_tool(self, tool):
        self.current_tool = tool

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())
        elif event.button() == Qt.RightButton:
            if self.selection_rect.contains(event.pos()):
                self.dragging_selection = True
                self.drag_start = event.pos()
                self.drag_offset = self.selection_rect.topLeft() - self.drag_start
            else:
                self.selection_start = event.pos()
                self.selection_end = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_pos:
            painter = QPainter(self.pixmap())
            pen = QPen(self.brush.color, self.brush.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())
        elif event.buttons() & Qt.RightButton:
            if self.dragging_selection:
                delta = event.pos() - self.drag_start
                self.selection_rect.translate(delta)
                self.drag_start = event.pos()
                self.update()
            elif self.selection_start:
                self.selection_end = event.pos()
                self.update()
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.dragging_selection:
                self.dragging_selection = False
            elif self.selection_start and self.selection_end:
                self.selection_rect = QRect(self.selection_start, self.selection_end).normalized()
                self.update()
                self.selection_start = None
                self.selection_end = None
            self.resizing_selection = False
            self.resize_direction = None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.selection_rect.isNull():
            pen = QPen(Qt.black, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.selection_rect)

            self.draw_resize_handles(painter)

        if self.selection_start and self.selection_end:
            pen = QPen(Qt.red, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(self.selection_start, self.selection_end).normalized())

    def draw_resize_handles(self, painter):
        handle_size = 8
        handles = self.get_resize_handles()

        pen = QPen(Qt.black, 1)
        brush = QtGui.QBrush(Qt.white)
        painter.setPen(pen)
        painter.setBrush(brush)

        for handle in handles:
            painter.drawRect(handle)

    def get_resize_handles(self):
        handle_size = 8
        rect = self.selection_rect

        handles = [
            QRect(rect.topLeft() - QPoint(handle_size // 2, handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.topRight() - QPoint(handle_size // 2, handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.bottomLeft() - QPoint(handle_size // 2, handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.bottomRight() - QPoint(handle_size // 2, handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.topLeft() + QPoint(rect.width() // 2 - handle_size // 2, -handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.topLeft() + QPoint(-handle_size // 2, rect.height() // 2 - handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.bottomLeft() + QPoint(rect.width() // 2 - handle_size // 2, -handle_size // 2), QSize(handle_size, handle_size)),
            QRect(rect.topRight() + QPoint(-handle_size // 2, rect.height() // 2 - handle_size // 2), QSize(handle_size, handle_size)),
        ]

        return handles

    def update_cursor(self, pos):
        if not self.selection_rect.isNull():
            handles = self.get_resize_handles()
            for i, handle in enumerate(handles):
                if handle.contains(pos):
                    if i in [0, 3]:
                        self.setCursor(Qt.SizeFDiagCursor)
                    elif i in [1, 2]:
                        self.setCursor(Qt.SizeBDiagCursor)
                    elif i in [4, 6]:
                        self.setCursor(Qt.SizeVerCursor)
                    elif i in [5, 7]:
                        self.setCursor(Qt.SizeHorCursor)
                    return
            if self.selection_rect.contains(pos):
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def delete_selection(self):
        if not self.selection_rect.isNull():
            painter = QPainter(self.pixmap())
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.fillRect(self.selection_rect, Qt.white)
            painter.end()
            self.selection_rect = QRect()
            self.update()