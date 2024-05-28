import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QStackedWidget

class BrushInput:
    def __init__(self, brush, canvas):
        self.brush = brush
        self.canvas = canvas

    def update_brush_size(self, value):
        self.brush.size = value

class Brush:
    def __init__(self):
        self.size = 5
        self.color = QtGui.QColor(0, 0, 0)

    def set_color(self, color):
        self.color = color

class Eraser:
    def __init__(self):
        self.size = 5

class Sidebar(QtWidgets.QWidget):
    def __init__(self, canvas):
        super().__init__()

        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        brushicon = os.path.join(script_dir, 'icons', 'brushicon.png')
        erasericon = os.path.join(script_dir, 'icons', 'erasericon.png')

        self.brush_button = QPushButton('')
        self.brush_button.setToolTip('Select The Brush tool')
        self.brush_button.setFixedHeight(30)
        self.brush_button.setFixedWidth(80)
        self.brush_button.setIcon(QIcon(brushicon))
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton('')
        self.eraser_button.setToolTip('Select The Eraser Tool')
        self.eraser_button.setFixedHeight(30)
        self.eraser_button.setFixedWidth(80)
        self.eraser_button.setIcon(QIcon(erasericon))
        self.eraser_button.clicked.connect(self.set_eraser_tool)

        self.brush_thickness_label = QLabel("Thickness: 5")
        thickness_slider = QSlider(Qt.Horizontal)
        thickness_slider.setMinimum(1)
        thickness_slider.setMaximum(100)
        thickness_slider.setValue(5)
        thickness_slider.valueChanged.connect(lambda value: self.update_thickness_label(value))

        self.brush_size_label = QLabel("Size: 5")
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(lambda value: self.update_size_label(value))

        layout.addWidget(self.brush_button)
        layout.addWidget(self.eraser_button)
        layout.addWidget(self.brush_thickness_label)
        layout.addWidget(thickness_slider)
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(QPushButton("Choose color", self))

        layout.setAlignment(Qt.AlignTop)

        self.canvas = canvas
        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)

    def update_thickness_label(self, value):
        self.brush_thickness_label.setText(f"Thickness: {value}")

    def update_size_label(self, value):
        self.brush_size_label.setText(f"Size: {value}")

    def open_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brush.color = color
            self.brush.set_color(color)

    def set_brush_tool(self):
        self.active_tool = "Brush"
        self.brush_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.brush)

    def set_eraser_tool(self):
        self.active_tool = "Eraser"
        self.eraser_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.eraser)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.active_tool = None

    def initUI(self):
        self.setWindowTitle("Drawing app")
        self.setGeometry(150, 150, 650, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        central_widget.setLayout(main_layout)

        self.canvas = QWidget()  # Placeholder for your canvas
        sidebar = Sidebar(self.canvas)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.canvas)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

    def save(self):
        print("Save action triggered!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
