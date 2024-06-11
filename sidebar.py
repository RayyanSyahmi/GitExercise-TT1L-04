import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from brush import BrushInput, Brush, Eraser, EraserInput
import sys
import os

class BrushInput:
    def __init__(self, brush, canvas):
        self.brush = brush
        self.canvas = canvas

    def update_brush_size(self, size):
        self.brush.size = size
        self.canvas.update()


class Brush:
    def __init__(self):
        self.size = 20
        self.color = QtGui.QColor("#000000")

    def set_color(self, color):
        self.color = color


class EraserInput:
    def __init__(self, eraser, canvas):
        self.eraser = eraser
        self.canvas = canvas

    def update_eraser_size(self, size):
        self.eraser.size = size
        self.canvas.update()


class Eraser:
    def __init__(self):
        self.size = 20


class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.layers = []
        self.current_layer_index = 0
        self.layers_count = 0

    def add_layer(self):
        self.layers.append(QtWidgets.QPixmap(self.size()))
        self.current_layer_index = len(self.layers) - 1
        self.layers_count += 1

    def remove_layer(self):
        if self.layers_count > 1:
            del self.layers[self.current_layer_index]
            self.current_layer_index = max(0, self.current_layer_index - 1)
            self.layers_count -= 1

    def clear_layer(self):
        self.layers[self.current_layer_index].fill(QtCore.Qt.transparent)

    def undo(self):
        print("Undo action")

    def redo(self):
        print("Redo action")

    def set_tool(self, tool):
        pass

    def update_canvas(self):
        pass

class Sidebar(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        self.sidebar_layout = QVBoxLayout()  
        self.sidebar_layout.setSpacing(0)
        self.setsidebar_Layout(self.sidebar_layout)

        self.add_layer_button = QPushButton('Add Layer')
        self.add_layer_button.clicked.connect(self.add_layer)
        self.sidebar_layout.addWidget(self.add_layer_button)

        self.remove_layer_button = QPushButton('Remove Layer')
        self.remove_layer_button.clicked.connect(self.remove_layer)
        self.sidebar_layout.addWidget(self.remove_layer_button)

        self.layer_combo_box = QComboBox()
        self.layer_combo_box.currentIndexChanged.connect(self.change_current_layer)
        self.sidebar_layout.addWidget(self.layer_combo_box)

        self.brush_button = QPushButton("Brush")
        self.brush_button.clicked.connect(self.set_brush_tool)
        self.sidebar_layout.addWidget(self.brush_button)

        self.eraser_button = QPushButton("Eraser")
        self.eraser_button.clicked.connect(self.set_eraser_tool)
        self.sidebar_layout.addWidget(self.eraser_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.canvas.undo)
        self.sidebar_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.canvas.redo)
        self.sidebar_layout.addWidget(self.redo_button)

        self.setsidebar_Layout(self.sidebar_layout)
        self.update_layer_combo_box()

    def add_layer(self):
        new_layer_index = self.canvas.add_layer()
        self.layer_combo_box.addItem(f'Layer {new_layer_index}')
        self.layer_combo_box.setCurrentIndex(new_layer_index - 1)
        self.update_layer_combo_box()

    def remove_layer(self):
        self.canvas.remove_layer()
        self.layer_combo_box.removeItem(self.layer_combo_box.currentIndex())
        self.update_layer_combo_box()

    def change_current_layer(self, index):
        self.canvas.set_current_layer(index)

    def update_layer_combo_box(self):
        self.layer_combo_box.clear()
        for i in range(len(self.canvas.layers)):
            self.layer_combo_box.addItem(f'Layer {i + 1}')
        self.layer_combo_box.setCurrentIndex(self.canvas.current_layer_index)

    def set_brush_tool(self):
        self.canvas.set_tool(self.canvas.brush)

    def set_eraser_tool(self):
        self.canvas.set_tool(self.canvas.eraser)
        
class Sidebar(QtWidgets.QWidget):
    def __init__(self, canvas):
        self.prev_selected_color_button = None
        super().__init__()

        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)

        sidebar_layout = QtWidgets.QVBoxLayout()
        sidebar_layout.setSpacing(0)
        self.setLayout(sidebar_layout)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        brushicon = os.path.join(script_dir, 'icons', 'brushicon.png')
        erasericon = os.path.join(script_dir, 'icons', 'erasericon.png')
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')

        self.undo_button = QtWidgets.QPushButton()
        self.undo_button.setFixedSize(50, 50)
        self.undo_button.setIcon(QtGui.QIcon(undoicon))
        self.undo_button.setToolTip('Undo')
        self.undo_button.clicked.connect(canvas.undo)

        self.redo_button = QtWidgets.QPushButton()
        self.redo_button.setFixedSize(50, 50)
        self.redo_button.setIcon(QtGui.QIcon(redoicon))
        self.redo_button.setToolTip('Redo')
        self.redo_button.clicked.connect(canvas.redo)

        self.brush_button = QtWidgets.QPushButton()

        self.brush_button = QPushButton()  
        self.brush_button.setFixedSize(50, 50)
        self.brush_button.setIcon(QIcon(brushicon))  
        self.brush_button.setToolTip('Brush Tool')  # Add tooltip for brush button
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton()
        self.eraser_button.setFixedSize(50, 50)
        self.eraser_button.setIcon(QIcon(erasericon)) 
        self.eraser_button.setToolTip('Eraser Tool')  # Add tooltip for eraser button
        self.eraser_button.clicked.connect(self.set_eraser_tool)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.brush_button)
        button_layout.addWidget(self.eraser_button)
        button_layout.addWidget(self.undo_button)
        button_layout.addWidget(self.redo_button)
        button_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.quick_color1 = QPushButton()
        self.quick_color1.setFixedSize(30, 30)
        self.quick_color1.setStyleSheet("background-color: #000000")  # Black
        self.quick_color1.clicked.connect(lambda: self.set_brush_color(0))

        self.quick_color2 = QPushButton()
        self.quick_color2.setFixedSize(30, 30)
        self.quick_color2.setStyleSheet("background-color: #FFFFFF")  # White
        self.quick_color2.clicked.connect(lambda: self.set_brush_color(1))

        self.quick_color3 = QPushButton()
        self.quick_color3.setFixedSize(30, 30)
        self.quick_color3.setStyleSheet("background-color: #007300")  # Green
        self.quick_color3.clicked.connect(lambda: self.set_brush_color(2))

        self.quick_color4 = QPushButton()
        self.quick_color4.setFixedSize(30, 30)
        self.quick_color4.setStyleSheet("background-color: #FFFF00")  # Yellow
        self.quick_color4.clicked.connect(lambda: self.set_brush_color(3))

        quick_color_layout = QtWidgets.QHBoxLayout()
        quick_color_layout.addWidget(self.quick_color1)
        quick_color_layout.addWidget(self.quick_color2)
        quick_color_layout.addWidget(self.quick_color3)
        quick_color_layout.addWidget(self.quick_color4)

        quick_color_layout.addSpacing(2)
        quick_color_widget = QtWidgets.QWidget()
        quick_color_widget.setLayout(quick_color_layout)

        self.brush_size_label = QtWidgets.QLabel("Size: 20")

        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(20)
        size_slider.valueChanged.connect(self.update_slider_label)
        
        self.color_button = QPushButton('Choose color')
        self.color_button.clicked.connect(lambda: self.open_color_dialog(self.color_button))
        
        self.add_layer_button = QPushButton('Add Layer')
        self.add_layer_button.clicked.connect(self.add_layer)

        self.remove_layer_button = QPushButton('Remove Layer')
        self.remove_layer_button.clicked.connect(self.remove_layer)

        self.layer_combo_box = QtWidgets.QComboBox()
        self.layer_combo_box.addItem("Layer 1")
        self.layer_combo_box.currentIndexChanged.connect(self.change_current_layer)
        self.layer_combo_box.show()

        self.clear_layer_button = QPushButton('Clear Layer')
        self.clear_layer_button.clicked.connect(self.clear_layer)

        self.fill_color_button = QPushButton('Fill in')
        self.fill_color_button.clicked.connect(self.fill_color)

        self.pickout_color_button = QPushButton('Pick color')
        self.pickout_color_button.clicked.connect(self.pickout_color)

        sidebar_layout.addLayout(button_layout)
        sidebar_layout.addWidget(self.brush_size_label)
        sidebar_layout.addWidget(size_slider)
        sidebar_layout.addWidget(self.color_button)
        sidebar_layout.addWidget(quick_color_widget)
        sidebar_layout.addWidget(self.layer_combo_box)
        sidebar_layout.addWidget(self.add_layer_button)
        sidebar_layout.addWidget(self.remove_layer_button)
        sidebar_layout.addWidget(self.clear_layer_button)
        sidebar_layout.addWidget(self.fill_color_button)
        sidebar_layout.addWidget(self.pickout_color_button)

        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(5)

        self.canvas = canvas
        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        self.eraser_size_input = EraserInput(self.eraser, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)
        self.eraser_button.clicked.connect(self.set_eraser_tool)

        self.hide()

        self.custom_colors = [QtGui.QColor("#000000"), QtGui.QColor("#FFFFFF"), QtGui.QColor("#007300"), QtGui.QColor("#FFFF00")]
        self.selected_color = self.custom_colors[0]

        self.set_brush_color(0)
        self.set_brush_tool()
        
    def set_brush_color(self, index):
        color = self.custom_colors[index]
        self.brush.color = color
        self.brush.set_color(color)
        self.selected_color = color

        if self.prev_selected_color_button:
            self.prev_selected_color_button.setStyleSheet(self.prev_selected_color_button.original_style)

        if index == 0:
            self.quick_color1.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
            self.quick_color1.original_style = "background-color: {};".format(color.name())
        elif index == 1:
            self.quick_color2.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
            self.quick_color2.original_style = "background-color: {};".format(color.name())
        elif index == 2:
            self.quick_color3.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
            self.quick_color3.original_style = "background-color: {};".format(color.name())
        elif index == 3:
            self.quick_color4.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
            self.quick_color4.original_style = "background-color: {};".format(color.name())

        self.prev_selected_color_button = self.quick_color1 if index == 0 else \
                                        self.quick_color2 if index == 1 else \
                                        self.quick_color3 if index == 2 else \
                                        self.quick_color4
    
    def get_selected_color(self):
        return self.selected_color

    def update_slider_label(self, value):
        self.brush_size_label.setText("Size: {}".format(value))

    
    def open_color_dialog(self, sender=None):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.brush.color = color
            self.brush.set_color(color)

            if self.prev_selected_color_button:
                self.prev_selected_color_button.setStyleSheet(self.prev_selected_color_button.original_style)

            if sender == self.color_button:
                if self.prev_selected_color_button:
                    self.prev_selected_color_button.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
                    self.prev_selected_color_button.original_style = "background-color: {};".format(color.name())
                self.prev_selected_color_button = None
            elif sender == self.quick_color1:
                self.quick_color1.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
                self.quick_color1.original_style = "background-color: {};".format(color.name())
                self.prev_selected_color_button = self.quick_color1
            elif sender == self.quick_color2:
                self.quick_color2.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
                self.quick_color2.original_style = "background-color: {};".format(color.name())
                self.prev_selected_color_button = self.quick_color2
            elif sender == self.quick_color3:
                self.quick_color3.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
                self.quick_color3.original_style = "background-color: {};".format(color.name())
                self.prev_selected_color_button = self.quick_color3
            elif sender == self.quick_color4:
                self.quick_color4.setStyleSheet("background-color: {}; border: 2px solid #d5d5d5;".format(color.name()))
                self.quick_color4.original_style = "background-color: {};".format(color.name())
                self.prev_selected_color_button = self.quick_color4
    
    def set_brush_tool(self):
        self.active_tool = "Brush"
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: white; border: 2px solid #000000;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.brush.color = self.selected_color
        self.brush.set_color(self.selected_color)
        self.canvas.set_tool(self.brush)

    def set_eraser_tool(self):
        self.active_tool = "Eraser"
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: white; border: 2px solid #000000;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.eraser)

    def add_layer(self):
        new_layer_index = self.canvas.add_layer()
        self.layer_combo_box.addItem(f"Layer {new_layer_index}")

    def remove_layer(self):
        current_index = self.layer_combo_box.currentIndex()
        if current_index >= 0:
            self.layer_combo_box.removeItem(current_index)
            self.canvas.remove_layer()

    def clear_layer(self):
        self.canvas.clear_layer()

    def change_current_layer(self, index):
        self.canvas.set_current_layer(index)

    def update_layer_combo_box(self):
        self.layer_combo_box.clear()
        for i in range(len(self.canvas.layers)):
            self.layer_combo_box.addItem(f'Layer {i + 1}')
        self.layer_combo_box.setCurrentIndex(self.canvas.current_layer_index)

    def fill_color(self):
        pass

    def pickout_color(self, color):
        painter = QtGui.QPainter(self.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(color)
        brush.setStyle(Qt.SolidPattern)

    def start_drawing(self):
        if self.canvas.layers_count > 0:
            # Allow the user to draw
            pass
        else:
            print("Please create a layer before drawing")

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
