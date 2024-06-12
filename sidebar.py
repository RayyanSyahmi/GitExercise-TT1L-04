import PyQt5 
import math
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

        self.layers = []
        self.current_layer_index = 0

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

        self.shape_combo_box = QComboBox()
        self.shape_combo_box.addItem('Pen')
        self.shape_combo_box.addItem('Square')
        self.shape_combo_box.addItem('Triangle')
        self.shape_combo_box.addItem('Rectangle')
        self.shape_combo_box.addItem('Circle')
        self.shape_combo_box.addItem('Star')
        self.shape_combo_box.currentIndexChanged.connect(self.change_shape)


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

        self.add_layer()
    
    def set_background(self, image_path):
        if os.path.exists("C:/Users/User/OneDrive/Desktop/f7188d253ebe032b9eb678e43e78c2bf.jpg"):
            background_pixmap = QPixmap("C:/Users/User/OneDrive/Desktop/f7188d253ebe032b9eb678e43e78c2bf.jpg")
            background_pixmap = background_pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(background_pixmap))
            self.setPalette(palette)
        
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
        layer_index = len(self.layers)
        layer = QImage(1000, 800, QImage.Format_ARGB32)
        layer.fill(Qt.transparent)
        self.layers.append(layer)

        self.layer_combo_box.addItem(f"Layer {layer_index + 1}")
        self.layer_combo_box.setCurrentIndex(layer_index)

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
        if len(self.layers) > 1:
            self.layers.pop()
            self.layer_combo_box.removeItem(len(self.layers))
            self.current_layer_index = min(self.current_layer_index, len(self.layers) - 1)

    def clear_layer(self):
        if self.current_layer_index < len(self.layers):
            self.layers[self.current_layer_index].fill(Qt.transparent)

    def change_current_layer(self, index):
        if index < len(self.layer_opacities):
            self.current_layer_index = index

    def update_layer_combo_box(self):
        self.layer_combo_box.clear()
        for i in range(len(self.canvas.layers)):
            self.layer_combo_box.addItem(f'Layer {i + 1}')
        self.layer_combo_box.setCurrentIndex(self.canvas.current_layer_index)

    def change_current_layer(self, index):
        self.current_layer_index = index

    def change_shape(self, index):
        shapes = ["Pen", "Square", "Triangle", "Rectangle", "Circle", "Star"]
        self.shape = shapes[index]

    def change_shape_size(self, size):
        self.shape_size = size

    def draw_shape(self, pos):
        painter = QPainter(self.layers[self.current_layer_index])
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)

        if self.shape == "Square":
            painter.drawRect(QRect(pos.x() - self.shape_size // 2, pos.y() - self.shape_size // 2, self.shape_size, self.shape_size))
        elif self.shape == "Triangle":
            path = QPainterPath()
            path.moveTo(pos.x(), pos.y() - self.shape_size // 2)
            path.lineTo(pos.x() - self.shape_size // 2, pos.y() + self.shape_size // 2)
            path.lineTo(pos.x() + self.shape_size // 2, pos.y() + self.shape_size // 2)
            path.closeSubpath()
            painter.drawPath(path)
        elif self.shape == "Rectangle":
            painter.drawRect(QRect(pos.x() - self.shape_size, pos.y() - self.shape_size // 2, self.shape_size * 2, self.shape_size))
        elif self.shape == "Circle":
            painter.drawEllipse(pos, self.shape_size // 2, self.shape_size // 2)
        elif self.shape == "Star":
            path = QPainterPath()
            outer_radius = self.shape_size
            inner_radius = outer_radius * 0.5
            for i in range(10):
                angle = i * math.pi / 5  # 36 degrees
                if i % 2 == 0:
                    x = pos.x() + outer_radius * math.cos(angle)
                    y = pos.y() - outer_radius * math.sin(angle)
                else:
                    x = pos.x() + inner_radius * math.cos(angle)
                    y = pos.y() - inner_radius * math.sin(angle)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.closeSubpath()
            painter.drawPath(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            local_pos = self.canvas_label.mapFrom(self, event.pos())
            if self.shape == "Pen":
                self.draw_brush(local_pos)
            else:
                self.draw_shape(local_pos)
            self.update_canvas()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.shape == "Pen":
            local_pos = self.canvas_label.mapFrom(self, event.pos())
            self.draw_brush(local_pos)
            self.update_canvas()

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
