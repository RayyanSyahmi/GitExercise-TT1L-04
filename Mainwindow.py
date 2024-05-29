import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
from sidebar import Sidebar
from canvasclass import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vbox_layout = QVBoxLayout()
        self.central_widget.setLayout(self.vbox_layout)

        self.main_h_layout = QHBoxLayout()
        self.vbox_layout.addLayout(self.main_h_layout)

        self.canvas = Canvas()
        self.sidebar = Sidebar(self.canvas)
        self.main_h_layout.addWidget(self.sidebar)
        self.main_h_layout.addWidget(self.canvas)

        self.move(0, 0)
        self.show()

app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 9))
app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
