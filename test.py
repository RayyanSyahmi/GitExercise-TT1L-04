import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setSceneRect(0, 0, 400, 400)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.setWindowTitle("Zoom Example")
        self.setGeometry(100, 100, 800, 600)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
