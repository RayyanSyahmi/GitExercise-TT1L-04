import sys
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
        self.setPixmap(pixmap)
        self.update()
        self.brush = Brush()
        self.eraser = Eraser()
        self.current_tool = None
        self.drawing_points = []
        self.selection_rect = None
        self.selection_start = None
        self.selection_end = None
        self.setStyleSheet("background-color: white;")
        self.setMouseTracking(True)
        self.resizing = False
        self.resize_direction = None
        self.creating_selection = False

    def set_tool(self, tool):
        self.current_tool = tool

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_pixmap = QtGui.QPixmap(self.size())
        new_pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(new_pixmap)
        painter.drawPixmap(0, 0, self.pixmap())
        self.setPixmap(new_pixmap)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.is_on_resize_handle(event.pos()):
                self.resizing = True
                self.resize_start = event.pos()
                self.resize_direction = self.get_resize_direction(event.pos())
            else:
                self.last_pos = event.pos()
                self.drawing_points.append(event.pos())
        elif event.button() == QtCore.Qt.RightButton:
            self.selection_start = event.pos()
            self.creating_selection = True

    def mouseMoveEvent(self, event):
        if self.resizing and event.buttons() & QtCore.Qt.LeftButton:
            self.resize_selection(event.pos())
        elif event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            painter = QtGui.QPainter(self.pixmap())
            pen = QtGui.QPen(self.brush.color, self.brush.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()
            self.drawing_points.append(event.pos())
        elif event.buttons() & QtCore.Qt.RightButton and self.selection_start:
            self.selection_end = event.pos()
            self.update()
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.RightButton and self.selection_start and self.selection_end:
            self.selection_rect = QRect(self.selection_start, self.selection_end).normalized()
            self.creating_selection = False
            self.update()
        elif event.button() == QtCore.Qt.LeftButton:
            self.resizing = False
            self.resize_direction = None
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.creating_selection and self.selection_start and self.selection_end:
            pen = QPen(Qt.black, 1, Qt.DotLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(self.selection_start, self.selection_end).normalized())
        elif self.selection_rect:
            pen = QPen(Qt.black, 1, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.selection_rect)
            self.draw_resize_handles(painter)

    def draw_resize_handles(self, painter):
        if self.selection_rect:
            handle_size = 8
            handles = self.get_resize_handles()

            pen = QPen(Qt.black, 1)
            brush = QBrush(Qt.white)
            painter.setPen(pen)
            painter.setBrush(brush)

            for handle in handles:
                painter.drawRect(handle)

    def get_resize_handles(self):
        handle_size = 8
        rect = self.selection_rect

        if not rect:
            return []

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
        if self.selection_rect and not self.selection_rect.isNull():
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
        else:
            self.setCursor(Qt.ArrowCursor)

    def is_on_resize_handle(self, pos):
        if not self.selection_rect:
            return False
        return any(handle.contains(pos) for handle in self.get_resize_handles())

    def get_resize_direction(self, pos):
        handles = self.get_resize_handles()
        directions = ['nw', 'ne', 'sw', 'se', 'n', 's', 'w', 'e']
        for i, handle in enumerate(handles):
            if handle.contains(pos):
                return directions[i]
        return None

    def resize_selection(self, pos):
        delta = pos - self.resize_start
        if self.resize_direction == 'nw':
            self.selection_rect.setTopLeft(self.selection_rect.topLeft() + delta)
        elif self.resize_direction == 'ne':
            self.selection_rect.setTopRight(self.selection_rect.topRight() + QPoint(delta.x(), 0))
        elif self.resize_direction == 'sw':
            self.selection_rect.setBottomLeft(self.selection_rect.bottomLeft() + QPoint(0, delta.y()))
        elif self.resize_direction == 'se':
            self.selection_rect.setBottomRight(self.selection_rect.bottomRight() + delta)
        elif self.resize_direction == 'n':
            self.selection_rect.setTop(self.selection_rect.top() + delta.y())
        elif self.resize_direction == 's':
            self.selection_rect.setBottom(self.selection_rect.bottom() + delta.y())
        elif self.resize_direction == 'w':
            self.selection_rect.setLeft(self.selection_rect.left() + delta.x())
        elif self.resize_direction == 'e':
            self.selection_rect.setRight(self.selection_rect.right() + delta.x())

        self.selection_rect = self.selection_rect.normalized()
        self.resize_start = pos
        self.update()

    def delete_selection(self):
        if self.selection_rect:
            painter = QPainter(self.pixmap())
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.fillRect(self.selection_rect, Qt.white)
            painter.end()
            self.selection_rect = None
            self.selection_start = None
            self.selection_end = None
            self.update()

    def adjustSize(self):
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(0, 0, self.pixmap())
        self.setPixmap(pixmap)
        self.update()

    def save(self, file_path):
        self.pixmap().save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Canvas()
    window.show()
    sys.exit(app.exec_())

