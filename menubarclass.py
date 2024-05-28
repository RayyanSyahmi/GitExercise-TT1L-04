import PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from canvasclass import Canvas
import sys
import os

class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        # File Menu
        file_menu = self.addMenu('File')
        file_menu.addAction("New")
        file_menu.addAction("Open")
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        # Undo and Redo Actions
        script_dir = os.path.dirname(os.path.abspath(__file__))
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')

        undo_action = QAction(QIcon(undoicon), 'Undo', self)
        redo_action = QAction(QIcon(redoicon), 'Redo', self)

        # Adding tooltips to Undo and Redo Actions
        undo_action.setToolTip('Undo ')
        redo_action.setToolTip('Redo ')

        # Adding Undo and Redo Actions to the MenuBar
        self.addAction(undo_action)
        self.addAction(redo_action)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.canvas.save(filePath)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = Canvas()
    window = QMainWindow()
    menubar = MyMenuBar(canvas)
    window.setMenuBar(menubar)
    window.setCentralWidget(canvas)
    window.setWindowTitle("Drawing App")
    window.setGeometry(150, 150, 650, 450)
    window.show()
    sys.exit(app.exec_())
