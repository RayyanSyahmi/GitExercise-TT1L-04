import PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from canvas import Canvas
import sys
import os

class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

        # File menu
        file_menu = self.addMenu("File")

        # Save action
        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.save)
        file_menu.addAction(saveAction)

        # Path to icons
        script_dir = os.path.dirname(os.path.abspath(__file__))
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')
        icons_folder = os.path.dirname(os.path.abspath(__file__))
        undoicon = os.path.join(icons_folder, 'icons', 'undoicon.png')
        redoicon = os.path.join(icons_folder,'icons', 'redoicon.png')

        # Undo action
        undo_action = QAction(QIcon(undoicon), 'Undo', self)
        undo_action.triggered.connect(self.canvas.undo)
        self.addAction(undo_action)

        # Redo action
        redo_action = QAction(QIcon(redoicon), 'Redo', self)
        redo_action.triggered.connect(self.canvas.redo)
        self.addAction(redo_action)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

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