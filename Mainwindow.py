import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
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

        self.sidebar_toggle_action = QAction("Tools", self)
        self.sidebar_toggle_action.triggered.connect(self.toggle_sidebar)
        self.menu_bar.addAction(self.sidebar_toggle_action)

        self.move(0, 0)
        self.show()

    def toggle_sidebar(self):
        if self.dock_widget.isVisible():
            self.dock_widget.hide()
            self.sidebar_toggle_action.setText("Tools")
        else:
            self.dock_widget.show()
            self.sidebar_toggle_action.setText("Tools")
            
app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 9))
app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
