import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Drawing app")
        self.setGeometry(150, 150, 650, 450)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        file_menu.addAction(save_action)

    def save(self):
        print("Save action triggered!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
