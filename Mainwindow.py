import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from menubarclass import MyMenuBar
from sidebar import Sidebar
from brushes import Brush
from canvasclass import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("MainWindow initialized")
        self.setWindowTitle("Paint app")
        self.setGeometry(0, 0, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vbox_layout = QVBoxLayout()
        self.central_widget.setLayout(self.vbox_layout)

        self.main_h_layout = QHBoxLayout()
        self.vbox_layout.addLayout(self.main_h_layout)

        self.sidebar = Sidebar()
        self.main_h_layout.addWidget(self.sidebar)

        self.brush = Brush()
        self.canvas = Canvas()
        self.canvas.brush = self.brush
        self.main_h_layout.addWidget(self.canvas)

        self.menu_bar = MyMenuBar()
        self.setMenuBar(self.menu_bar)

        self.show()
        
        print("MainWindow initialized complete")

app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec_())