import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from brushes import Brush, BrushSizeInput

class PaintCanvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QtGui.QPixmap(800, 500))
        self.pixmap().fill(QtCore.Qt.white)

        self.last_pos = None
        self.brush = Brush()

        self.brush_size_input = BrushSizeInput(self.brush)
        self.brush_size_input.setGeometry(10, 10, 80, 20)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)
        self.setLayout(layout)

        # Connect the textChanged signal to the update_brush_size method
        self.brush_size_input.brush_size_input.textChanged.connect(self.update_brush_size)

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
            painter.setBrush(QtCore.Qt.black)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()

app = QtWidgets.QApplication(sys.argv)

window = PaintCanvas()
window.show()

app.exec_()