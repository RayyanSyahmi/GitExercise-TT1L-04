import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QSlider, QColorDialog, QComboBox

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
    currentLayerChanged = QtCore.pyqtSignal(int)

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.initUI()

    def initUI(self):
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        brushicon = os.path.join(script_dir, 'icons', 'brushicon.png')
        erasericon = os.path.join(script_dir, 'icons', 'erasericon.png')

        self.brush_button = QPushButton(' ')
        self.brush_button.setToolTip('Select The Brush tool')
        self.brush_button.setFixedHeight(30)
        self.brush_button.setFixedWidth(80)
        self.brush_button.setIcon(QIcon(brushicon))
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton(' ')
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
        thickness_slider.valueChanged.connect(self.update_thickness_label)

        self.brush_size_label = QLabel("Size: 5")
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(self.update_size_label)

        delete_selection_button = QPushButton("Delete Selection")
        delete_selection_button.clicked.connect(self.canvas.delete_selection)

        fill_color_button = QPushButton('Fill Color')
        fill_color_button.clicked.connect(self.open_color_dialog)

        self.layer_label = QLabel("Current Layer:")
        self.layer_combo_box = QComboBox()
        self.layer_combo_box.addItems([str(i) for i in range(1)])  # Initial layer
        self.layer_combo_box.currentIndexChanged.connect(self.layer_changed)

        self.add_layer_button = QPushButton("Add Layer")
        self.add_layer_button.clicked.connect(self.add_layer)

        self.remove_layer_button = QPushButton("Remove Layer")
        self.remove_layer_button.clicked.connect(self.remove_layer)

        layout.addWidget(self.brush_button)
        layout.addWidget(self.eraser_button)
        layout.addWidget(self.brush_thickness_label)
        layout.addWidget(thickness_slider)
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(QPushButton("Choose color", self))
        layout.addWidget(delete_selection_button)
        layout.addWidget(fill_color_button)
        layout.addWidget(self.layer_label)
        layout.addWidget(self.layer_combo_box)
        layout.addWidget(self.add_layer_button)
        layout.addWidget(self.remove_layer_button)

        layout.setAlignment(Qt.AlignTop)

        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)

    def update_thickness_label(self, value):
        self.brush_thickness_label.setText(f"Thickness: {value}")

    def update_size_label(self, value):
        self.brush_size_label.setText(f"Size: {value}")

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.fill_color = color

    def set_brush_tool(self):
        self.canvas.set_tool(self.brush)

    def set_eraser_tool(self):
        self.canvas.set_tool(self.eraser)

    def change_current_layer(self, index):
        self.layer_combo_box.setCurrentIndex(index)

    def add_layer(self):
        new_layer_index = self.layer_combo_box.count()
        self.layer_combo_box.addItem(str(new_layer_index))
        self.canvas.add_layer(new_layer_index)

    def remove_layer(self):
        current_index = self.layer_combo_box.currentIndex()
        if current_index >= 0:
            self.layer_combo_box.removeItem(current_index)
            self.canvas.remove_layer()

    def layer_changed(self, index):
        self.currentLayerChanged.emit(index)
        self.canvas.change_current_layer(index)
