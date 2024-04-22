import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class PaintCanvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QtGui.QPixmap(800, 600)) # Set the canvas size to 1200x900
        self.pixmap().fill(QtCore.Qt.white)
        self.last_pos = None
        self.brush_radius = 5
        self.brush_offset = QtCore.QPoint(0, 0)

        self.brush_size_input = QtWidgets.QLineEdit(self)
        self.brush_size_input.setPlaceholderText("Brush size")
        self.brush_size_input.setGeometry(10, 10, 80, 20)
        self.brush_size_input.returnPressed.connect(self.set_brush_radius_from_input)

    def set_brush_radius_from_input(self):
        try:
            self.brush_radius = int(self.brush_size_input.text())
            self.brush_size_input.clear()
        except ValueError:
            pass

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.last_pos:
            painter = QtGui.QPainter(self.pixmap())
            painter.setPen(QtGui.QPen(QtCore.Qt.black, self.brush_radius * 2))
            painter.setBrush(QtCore.Qt.black)
            painter.drawLine(self.last_pos, event.pos())
            painter.end()
            self.update()
            self.last_pos = event.pos()

app = QtWidgets.QApplication(sys.argv)
window = PaintCanvas()
window.show()
app.exec_()