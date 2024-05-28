<<<<<<< HEAD
import PyQt5
=======
import PyQt5 
>>>>>>> e830c5d7e78df9d2ee814107ab8a88628a962649
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from canvasclass import Canvas
import sys
<<<<<<< HEAD
import os
=======
>>>>>>> e830c5d7e78df9d2ee814107ab8a88628a962649

class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

<<<<<<< HEAD
        # File Menu
=======
>>>>>>> e830c5d7e78df9d2ee814107ab8a88628a962649
        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")

<<<<<<< HEAD
        save_action = QAction("Save", self)
        self.save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save)

        # Undo and Redo Actions
        script_dir = os.path.dirname(os.path.abspath(__file__))
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')

        undo_action = QAction(QIcon(undoicon), 'Undo', self)
        redo_action = QAction(QIcon(redoicon), 'Redo', self)

        # Adding Undo and Redo Actions to the MenuBar
        self.addAction(undo_action)
        self.addAction(redo_action)
=======
        saveAction = QAction("Save", self)
        self.save_action = file_menu.addAction("Save")
        saveAction.triggered.connect(self.save)
>>>>>>> e830c5d7e78df9d2ee814107ab8a88628a962649

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
<<<<<<< HEAD
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
=======
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    
        if filePath == "":
            return
        self.canvas.save(filePath)
>>>>>>> e830c5d7e78df9d2ee814107ab8a88628a962649
