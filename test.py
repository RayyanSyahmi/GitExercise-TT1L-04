import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QColorDialog
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt

class DrawingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.colors = [Qt.red, Qt.blue, Qt.green, Qt.yellow, Qt.black]
        self.current_color = self.colors[0]
        self.last_clicked_button = None
        self.canvas_color = self.colors[0]
        self.button_colors = {}

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        for i, color in enumerate(self.colors):
            button = QPushButton()
            button.setFixedSize(50, 50)
            button.setStyleSheet(f"background-color: {self.getColorString(color)}")
            button.clicked.connect(lambda checked, button=button: self.changeColor(button))
            layout.addWidget(button)
            self.button_colors[button] = color

        color_button = QPushButton("Custom Color")
        color_button.clicked.connect(self.showColorDialog)
        layout.addWidget(color_button)

        self.show()

    def changeColor(self, button):
        color = self.button_colors[button]
        self.canvas_color = color
        self.update()

    def showColorDialog(self):
        if self.last_clicked_button:
            color = QColorDialog.getColor()
            if color.isValid():
                self.last_clicked_button.setStyleSheet(f"background-color: {color.name()}")
                self.button_colors[self.last_clicked_button] = color.rgb()
                self.canvas_color = color.rgb()
                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(self.canvas_color))
        painter.drawRect(50, 50, 700, 500)

    def getColorString(self, color):
        if color == Qt.red:
            return "red"
        elif color == Qt.blue:
            return "blue"
        elif color == Qt.green:
            return "green"
        elif color == Qt.yellow:
            return "yellow"
        elif color == Qt.black:
            return "black"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DrawingApp()
    sys.exit(app.exec_())