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
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setSceneRect(0, 0, 400, 400)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

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

        self.color_button = QtWidgets.QPushButton("Choose color", self)
        self.color_button.setGeometry(self.brush_size_input.geometry().right() + 10, self.brush_size_input.geometry().top(), 20, 20)
        self.color_button.clicked.connect(self.choose_color)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)
        layout.addWidget(self.color_button)
        self.setLayout(layout)

        self.resizeEvent = self.resizeEvent

        #connects the textChanged signal to the update_brush_size method
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

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        #checks if mouse if pressed and checks last  positionf
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            #creates QPainter object and sets pixmap as the paint device
            painter = QtGui.QPainter(self.pixmap())
            #creates QPen with size and color from brush class
            pen = QtGui.QPen(QtGui.QPen(self.brush.color, self.brush.size))
            #sets properties of Qpainter to Qpen
            painter.setPen(pen)
            #draws line between last position and current position
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            #keep track of mouse movement
            self.last_pos = event.pos()

app = QtWidgets.QApplication(sys.argv)

window = PaintCanvas()
window.show()

app.exec_()