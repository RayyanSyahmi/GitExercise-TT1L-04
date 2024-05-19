import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class LayeredCanvas(QWidget):
    def __init__(self):
        super().__init__()

        self.layers = []
        self.current_layer_index = 0
        self.brush_size = 5
        self.brush_color = Qt.black
        self.shape = "NoPen"
        self.shape_size = 10

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Layered Canvas')
        self.setGeometry(100, 100, 400, 400)

        self.add_layer_button = QPushButton('Add Layer')
        self.add_layer_button.clicked.connect(self.add_layer)

        self.remove_layer_button = QPushButton('Remove Layer')
        self.remove_layer_button.clicked.connect(self.remove_layer)

        self.clear_layer_button = QPushButton('Clear Layer')
        self.clear_layer_button.clicked.connect(self.clear_layer)

        self.layer_combo_box = QComboBox()
        self.layer_combo_box.currentIndexChanged.connect(self.change_current_layer)

        self.brush_size_slider = QSlider(Qt.Horizontal)
        self.brush_size_slider.setMinimum(1)
        self.brush_size_slider.setMaximum(50)
        self.brush_size_slider.setValue(self.brush_size)
        self.brush_size_slider.valueChanged.connect(self.change_brush_size)

        self.brush_color_button = QPushButton('Brush Color')
        self.brush_color_button.clicked.connect(self.change_brush_color)

        self.shape_combo_box = QComboBox()
        self.shape_combo_box.addItem('No Pen')
        self.shape_combo_box.addItem('Pen')
        self.shape_combo_box.addItem('Square')
        self.shape_combo_box.addItem('Triangle')
        self.shape_combo_box.addItem('Rectangle')
        self.shape_combo_box.addItem('Circle')
        self.shape_combo_box.addItem('Star')
        self.shape_combo_box.currentIndexChanged.connect(self.change_shape)

        self.shape_size_slider = QSlider(Qt.Horizontal)
        self.shape_size_slider.setMinimum(1)
        self.shape_size_slider.setMaximum(50)
        self.shape_size_slider.setValue(self.shape_size)
        self.shape_size_slider.valueChanged.connect(self.change_shape_size)

        self.canvas_label = QLabel()
        self.canvas_label.setFixedSize(400, 400)
        self.canvas_label.setAlignment(Qt.AlignCenter)
        self.canvas_label.setStyleSheet("border: 2px solid black;")

        self.canvas_pixmap = QPixmap(400, 400)
        self.canvas_pixmap.fill(Qt.white)
        self.canvas_label.setPixmap(self.canvas_pixmap)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.canvas_label)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.add_layer_button)
        self.main_layout.addWidget(self.remove_layer_button)
        self.main_layout.addWidget(self.clear_layer_button)
        self.main_layout.addWidget(self.layer_combo_box)
        self.main_layout.addWidget(self.brush_size_slider)
        self.main_layout.addWidget(self.brush_color_button)
        self.main_layout.addWidget(self.shape_combo_box)
        self.main_layout.addWidget(self.shape_size_slider)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.add_layer()

        self.setMouseTracking(True)

    def add_layer(self):
        layer_index = len(self.layers)
        layer = QImage(400, 400, QImage.Format_ARGB32)
        layer.fill(Qt.transparent)
        self.layers.append(layer)
        
        self.layer_combo_box.addItem(f"Layer {layer_index + 1}")
        self.layer_combo_box.setCurrentIndex(layer_index)

    def remove_layer(self):
        if len(self.layers) > 1:
            self.layers.pop()
            self.layer_combo_box.removeItem(len(self.layers))
            self.current_layer_index = min(self.current_layer_index, len(self.layers) - 1)
            self.update_canvas()

    def clear_layer(self):
        if self.current_layer_index < len(self.layers):
            self.layers[self.current_layer_index].fill(Qt.transparent)
            self.update_canvas()

    def change_current_layer(self, index):
        self.current_layer_index = index
        self.update_canvas()

    def change_brush_size(self, size):
        self.brush_size = size

    def change_brush_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brush_color = color

    def change_shape(self, index):
        shapes = ["NoPen", "Pen", "Square", "Triangle", "Rectangle", "Circle", "Star"]
        self.shape = shapes[index]

    def change_shape_size(self, size):
        self.shape_size = size

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw_shape(event.pos())
            self.update_canvas()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.draw_shape(event.pos())
            self.update_canvas()

    def draw_shape(self, pos):
        painter = QPainter(self.layers[self.current_layer_index])
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)

        if self.shape == "Pen":
            painter.drawPoint(pos)
        elif self.shape == "Square":
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

    def update_canvas(self):
        self.canvas_pixmap.fill(Qt.white)
        painter = QPainter(self.canvas_pixmap)
        for layer in self.layers:
            painter.drawImage(0, 0, layer)
        painter.end()
        self.canvas_label.setPixmap(self.canvas_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LayeredCanvas()
    window.show()
    sys.exit(app.exec_())
