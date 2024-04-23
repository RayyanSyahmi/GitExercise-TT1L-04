import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from brushes import Brush, BrushSizeInput

class PaintCanvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setPixmap(QtGui.QPixmap(800, 600))
        self.pixmap().fill(QtCore.Qt.white)
        self.showMaximized()

        self.last_pos = None
        self.brush = Brush()

        self.brush_size_input = BrushSizeInput(self.brush)
        self.brush_size_input.setGeometry(10, 10, 80, 20)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)
        self.setLayout(layout)

        self.resizeEvent = self.resizeEvent

        #connects the textChanged signal to the update_brush_size method
        self.brush_size_input.brush_size_input.textChanged.connect(self.update_brush_size)

    def update_brush_size(self, text):
        try:
            self.brush.size = int(text)
            self.brush.set_size(self.brush.size)
        except ValueError:
            pass
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