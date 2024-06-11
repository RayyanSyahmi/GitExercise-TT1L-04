import PyQt5 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from brush import BrushInput, Brush, Eraser, EraserInput
import sys
import os

class Sidebar(QtWidgets.QWidget):
    def __init__(self, canvas):
        self.prev_selected_color_button = None
        super().__init__()

        #variables
        self.setFixedWidth(200)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.white)
        self.setPalette(palette)
        
        #layout
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        #import images
        icons_folder = os.path.dirname(os.path.abspath(__file__))
        brushicon = os.path.join(icons_folder, 'icons', 'brushicon.png')
        erasericon = os.path.join(icons_folder, 'icons', 'erasericon.png')
        fillicon =os.path.join(icons_folder, 'icons', 'fillicon.png')

        #tools button
        self.brush_button = QPushButton()  
        self.brush_button.setFixedSize(50, 50)
        self.brush_button.setIcon(QIcon(brushicon)) 
        self.brush_button.setIconSize(QSize(40, 40)) 
        self.brush_button.setToolTip('Brush Tool')
        self.brush_button.clicked.connect(self.set_brush_tool)

        self.eraser_button = QPushButton()
        self.eraser_button.setFixedSize(50, 50)
        self.eraser_button.setIcon(QIcon(erasericon))
        self.eraser_button.setIconSize(QSize(40, 40)) 
        self.eraser_button.setToolTip('Eraser Tool')
        self.eraser_button.clicked.connect(self.set_eraser_tool)

        self.fill_button = QPushButton()  
        self.fill_button.setFixedSize(50, 50)
        self.fill_button.setIcon(QIcon(fillicon))
        self.fill_button.setIconSize(QSize(40, 40))  
        self.fill_button.setToolTip('Fill Tool')

        #tools layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.brush_button)
        button_layout.addWidget(self.eraser_button)
        button_layout.addWidget(self.fill_button)
        button_layout.setAlignment(Qt.AlignLeft)

        #colors button
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

        #colors layout
        quick_color_layout = QtWidgets.QHBoxLayout()
        quick_color_layout.addWidget(self.quick_color1)
        quick_color_layout.addWidget(self.quick_color2)
        quick_color_layout.addWidget(self.quick_color3)
        quick_color_layout.addWidget(self.quick_color4)
        quick_color_layout.addSpacing(2)
        quick_color_widget = QtWidgets.QWidget()
        quick_color_widget.setLayout(quick_color_layout)

        #size label
        self.brush_size_label = QtWidgets.QLabel("Size: 20")
        #size slider
        size_slider = QtWidgets.QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(20)
        size_slider.valueChanged.connect(self.update_slider_label)
        
        #color dialog
        self.color_button = QPushButton('Choose color')
        self.color_button.clicked.connect(lambda: self.open_color_dialog(self.color_button))
        
        #layer combo box
        self.layer_combo_box = QtWidgets.QComboBox()
        self.layer_combo_box.currentIndexChanged.connect(self.change_current_layer)
        self.layer_combo_box.show()

        #layer buttons
        self.add_layer_button = QPushButton('Add Layer')
        self.add_layer_button.clicked.connect(self.add_layer)

        self.remove_layer_button = QPushButton('Remove Layer')
        self.remove_layer_button.clicked.connect(self.remove_layer)

        self.clear_layer_button = QPushButton('Clear Layer')
        self.clear_layer_button.clicked.connect(self.clear_layer)

        #add to sidebar
        layout.addLayout(button_layout)
        layout.addWidget(self.brush_size_label)
        layout.addWidget(size_slider)
        layout.addWidget(self.color_button)
        layout.addWidget(quick_color_widget)
        layout.addWidget(self.layer_combo_box)
        layout.addWidget(self.add_layer_button)
        layout.addWidget(self.remove_layer_button)
        layout.addWidget(self.clear_layer_button)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(5)

        self.canvas = canvas
        self.brush = Brush()
        self.eraser = Eraser()
        self.brush_size_input = BrushInput(self.brush, self.canvas)
        self.eraser_size_input = EraserInput(self.eraser, self.canvas)
        size_slider.valueChanged.connect(self.brush_size_input.update_brush_size)
        self.eraser_button.clicked.connect(self.set_eraser_tool)
        self.hide()

        #colors for quick select color
        self.quick_color1_color = "#000000"
        self.quick_color2_color = "#FFFFFF"
        self.quick_color3_color = "#007300"
        self.quick_color4_color = "#FFFF00"

        self.set_brush_color(0)
        self.set_brush_tool()
        
    def set_brush_color(self, index):
        if index == 0:
            color = self.quick_color1.palette().button().color()
        elif index == 1:
            color = self.quick_color2.palette().button().color()
        elif index == 2:
            color = self.quick_color3.palette().button().color()
        elif index == 3:
            color = self.quick_color4.palette().button().color()

        if color:
            self.brush.color = color
            self.brush.set_color(color)
            self.selected_color = color
        else:
            print("No color selected")

        if index == 0:
            self.prev_selected_color_button = self.quick_color1
        elif index == 1:
            self.prev_selected_color_button = self.quick_color2
        elif index == 2:
            self.prev_selected_color_button = self.quick_color3
        elif index == 3:
            self.prev_selected_color_button = self.quick_color4
    
    def open_color_dialog(self, sender=None):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.brush.color = color
            self.brush.set_color(color)

            if sender == self.color_button:
                if self.prev_selected_color_button:
                    self.prev_selected_color_button.setStyleSheet("background-color: {};".format(color.name()))
                self.prev_selected_color_button = None
            else:
                sender.setStyleSheet("background-color: {};".format(color.name()))
                if sender == self.quick_color1:
                    self.quick_color1_color = color.name()
                elif sender == self.quick_color2:
                    self.quick_color2_color = color.name()
                elif sender == self.quick_color3:
                    self.quick_color3_color = color.name()
                elif sender == self.quick_color4:
                    self.quick_color4_color = color.name()
                self.prev_selected_color_button = sender

    def update_slider_label(self, value):
        self.brush_size_label.setText("Size: {}".format(value))

    def set_brush_tool(self):
        self.active_tool = "Brush"
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: white; border: 2px solid #000000;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.fill_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.brush.color = self.selected_color
        self.brush.set_color(self.selected_color)
        self.canvas.set_tool(self.brush)

    def set_eraser_tool(self):
        self.active_tool = "Eraser"
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: white; border: 2px solid #000000;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.fill_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.canvas.set_tool(self.eraser)

    def set_fill_tool(self):
        self.active_tool = "Fill"
        self.fill_button.setStyleSheet("background-color: #f0f0f0; color: white; border: 2px solid #000000;")
        self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        self.fill.color = self.selected_color
        self.fill.set_color(self.selected_color)
        self.canvas.set_tool(self.fill)
        

    def add_layer(self):
        self.canvas.add_layer()
        self.layer_combo_box.addItem('Layer {}'.format(self.canvas.layers_count))
        self.layer_combo_box.setCurrentIndex(self.layer_combo_box.count() - 1)

    def change_current_layer(self, index):
        if index >= 0 and index < len(self.canvas.layers):
            self.current_layer_index = index
            print(f"Current layer index: {index}")
            if self.canvas.layers_count > 0:
                self.canvas.update_canvas()
                self.layer_combo_box.setItemText(index, f"Layer {index + 1}")
        else:
            print("Error: Layer index is out of range.")

    def remove_layer(self):
        if self.canvas.layers_count > 1:
            self.canvas.remove_layer()
            self.layer_combo_box.removeItem(self.layer_combo_box.currentIndex())

    def clear_layer(self):
        self.canvas.clear_layer()
        self.canvas.update_canvas()

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)