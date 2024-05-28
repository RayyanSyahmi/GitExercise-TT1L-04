import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from menubarclass import MyMenuBar
from sidebar import Sidebar
from canvasclass import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stacked_layout = QStackedLayout()
        self.central_widget.setLayout(self.stacked_layout)

        self.canvas = Canvas()
        self.sidebar = Sidebar(self.canvas)

        self.stacked_layout.addWidget(self.canvas)
        self.stacked_layout.addWidget(self.sidebar)

        self.menu_bar = MyMenuBar(self.canvas)
        self.setMenuBar(self.menu_bar)

        self.sidebar_toggle_action = QAction("Show sidebar", self)
        self.sidebar_toggle_action.triggered.connect(self.toggle_sidebar)
        self.menu_bar.addAction(self.sidebar_toggle_action)

        self.move(0, 0)
        self.show()

    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
            self.sidebar_toggle_action.setText("Show sidebar")
            self.stacked_layout.setCurrentWidget(self.canvas)
        else:
            self.sidebar.show()
            self.sidebar_toggle_action.setText("Hide sidebar")
            self.stacked_layout.setCurrentWidget(self.sidebar)

app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 9))
app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())