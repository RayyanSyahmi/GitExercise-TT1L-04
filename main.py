import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QPushButton, QHBoxLayout
import sys
import PyQt5 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import brushes
import canvas
import menu_bar

class PaintCanvas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setCentralWidget(QtWidgets.QLabel(self))
        self.centralWidget().setPixmap(QtGui.QPixmap(800, 600))
        self.centralWidget().pixmap().fill(QtCore.Qt.white)
        self.showMaximized()

        self.last_pos = None
        self.brush = brushes.Brush()

        self.brush_size_input = menu_bar.BrushSizeInput(self.brush)
        self.brush_size_input.setGeometry(10, 10, 80, 20)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.brush_size_input)

        self.setLayout(layout)

        #connects the textChanged signal to the update_brush_size method
        self.brush_size_input.brush_size_input.textChanged.connect(self.update_brush_size)

    def initUI(self):
        self.setWindowTitle("Drawing app")
        self.setGeometry(150, 150, 650, 450)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        file_menu.addAction(save_action)
        self.setMenuBar(menubar)

    def save(self):
        print("Save action triggered!")
    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.width(), self.height())
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(0, 0, self.centralWidget().pixmap())
        painter.end()
        self.centralWidget().setPixmap(pixmap)

        self.update()
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
            painter = QtGui.QPainter(self.centralWidget().pixmap())
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PaintCanvas()
    window.show()
    sys.exit(app.exec_())