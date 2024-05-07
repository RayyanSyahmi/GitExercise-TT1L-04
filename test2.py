import sys
from PyQt5 import QtCore, QtWidgets, QtGui 
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from brushes import Brush, BrushSizeInput

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
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


class BrushSizeInput(QtWidgets.QWidget):
    def __init__(self, brush):
        super().__init__()
        self.brush = brush
        self.brush_size_input = QtWidgets.QLineEdit(self)
        self.brush_size_input.setFixedWidth(80)
        self.brush_size_input.setAlignment(QtCore.Qt.AlignCenter)
        self.brush_size_input.setText("5")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)
        self.setLayout(layout)

        self.brush_size_input.textChanged.connect(self.update_brush_size)

    def update_brush_size(self, text):
        try:
            self.brush.size = int(text)
            self.brush.set_size(self.brush.size)
        except ValueError:
            pass

class ColorButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__("Choose color", parent)
        self.clicked.connect(self.open_color_dialog)

    def open_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.parent().brush.color = color
            self.parent().brush.set_color(color)

class PaintCanvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QtGui.QPixmap(800, 600))
        self.pixmap().fill(QtCore.Qt.white)
        self.showMaximized()
        self.canvas = Canvas()

        self.last_pos = None
        self.brush = Brush()

        self.brush_size_input = BrushSizeInput(self.brush)
        self.brush_size_input.setGeometry(10, 10, 80, 20)

        self.color_button = ColorButton(self)
        self.color_button.setGeometry(self.brush_size_input.geometry().right() + 10, self.brush_size_input.geometry().top(), 20, 20)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)
        layout.addWidget(self.color_button)
        self.setLayout(layout)

        self.resizeEvent = self.resizeEvent

        self.brush_size_input.brush_size_input.textChanged.connect(self.update_brush_size)

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.width(), self.height())
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(0, 0, self.pixmap())
        painter.end()
        self.setPixmap(pixmap)

        self.update()
    def update_brush_size(self, text):
        try:
            self.brush.size = int(text)
            self.brush.set_size(self.brush.size)
        except ValueError:
            pass
    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush.color = color

app = QtWidgets.QApplication(sys.argv)

window = PaintCanvas()
window.show()

app.exec_()