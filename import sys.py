import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit

class UndoButtonExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Undo Button Example')
        self.setGeometry(300, 300, 300, 200)

        self.entry = QLineEdit(self)
        self.entry.move(50, 50)

        self.previous_value = self.entry.text()
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.move(50, 100)
        self.undo_button.clicked.connect(self.undo)

    def undo(self):
        current_value = self.entry.text()
        if current_value != self.previous_value:
            self.previous_value = current_value
            self.entry.setText(self.previous_value[:-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UndoButtonExample()
    ex.show()
    sys.exit(app.exec_())