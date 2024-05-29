import sys
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QPushButton, QLineEdit

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

    def save_file(self):
        types = [("Text Files", "*.txt"),
                 ("All Files", "*.*"),
                 ("Png Files", "*.png"),
                 ("Jpeg Files", "*.jpg *.jpeg")]

        file_path, _ = QFileDialog.getSaveFileName(self,
                                                    "Drawing app saving",
                                                    "",
                                                    "Text Files (*.txt);;Png Files (*.png);;Jpeg Files (*.jpg *.jpeg)",
                                                    options=QFileDialog.DontUseNativeDialog)

        if file_path:
            data = self.entry.text()
            with open(file_path, mode='w') as file_writter:
                file_writter.write(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UndoButtonExample()
    ex.show()

    ex.save_file()

    sys.exit(app.exec_())