import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QAction, QColorDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drawing app")
        self.setGeometry(150, 150, 650, 450)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        brush_menu = menubar.addMenu('Brush')

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        size_action = QAction('Size', self)
        size_action.triggered.connect(self.change_size)

        color_action = QAction('Color', self)
        color_action.triggered.connect(self.change_color)

        file_menu.addAction(save_action)
        brush_menu.addAction(size_action)
        brush_menu.addAction(color_action)

    def change_size(self):
        size, ok = QInputDialog.getInt(self, "Change Brush Size", "Brush size:", 5, 1, 50)
        if ok:
            print(f"Brush size changed to: {size}")

    def change_color(self):
        color = QColorDialog.getColor(self)
        if color.isValid():
            print(f"Brush color changed to: {color.name()}")      

    def save(self):
        print("Save action triggered!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
