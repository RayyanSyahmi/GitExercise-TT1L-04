import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QDockWidget, QAction, QMenu
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QRect, QPoint
from menubarclass import MyMenuBar
from sidebar import Sidebar
from canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.sidebar = Sidebar(self.canvas)
        self.dock_widget = QDockWidget("Tools", self)
        self.dock_widget.setWidget(self.sidebar)
        self.dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

        self.menu_bar = MyMenuBar(self.canvas)
        self.setMenuBar(self.menu_bar)

        self.sidebar_toggle = QAction("Tools", self)
        self.sidebar_toggle.triggered.connect(self.toggle_sidebar)
        self.menu_bar.addAction(self.sidebar_toggle)

        self.move(0, 0)
        self.show()

    def toggle_sidebar(self):
        if self.dock_widget.isVisible():
            self.dock_widget.hide()
            self.sidebar_toggle.setText("Show Tools")
        else:
            self.dock_widget.show()
            self.sidebar_toggle.setText("Hide Tools")

    def fill_selection(self, start, end):
        if start and end:
            selection_rect = QRect(start, end)
            for layer in self.layers:
                painter = QtGui.QPainter(layer)
                painter.setCompositionMode(QPainter.CompositionMode_Source)
                painter.fillRect(selection_rect, self.fill_color)
                painter.end()
            self.update_canvas()

    def fill(self, point):
        target_color = self.canvas.pixmap().toImage().pixelColor(point)
        if target_color == self.canvas.brush.color:
            return  # No need to fill if the target color is the same as the fill color

        stack = [point]
        while stack:
            current_point = stack.pop()
            x, y = current_point.x(), current_point.y()
            if x < 0 or y < 0 or x >= self.canvas.pixmap().width() or y >= self.canvas.pixmap().height():
                continue

            current_color = self.canvas.pixmap().toImage().pixelColor(current_point)
            if current_color == target_color:
                painter = QtGui.QPainter(self.canvas.pixmap())
                painter.setPen(self.canvas.brush.color)
                painter.drawPoint(current_point)
                painter.end()

                stack.append(QPoint(x + 1, y))
                stack.append(QPoint(x - 1, y))
                stack.append(QPoint(x, y + 1))
                stack.append(QPoint(x, y - 1))

        self.canvas.update()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        fill_action = menu.addAction("Fill Selection")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == fill_action:
            self.fill_selection(self.selection_start, self.selection_end)

app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 9))
app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
