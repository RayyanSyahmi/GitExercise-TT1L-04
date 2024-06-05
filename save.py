import sys
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QFileDialog 
import keyboard  # type: ignore

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

   
        file_menu = self.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")

        saveAction = QAction("Save", self) # type: ignore
        saveAction.triggered.connect(self.save)
        self.save_action = file_menu.addAction(saveAction)

    def save(self):
        print("Save button pressed")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    

        if file_path: # type: ignore
            data = self.entry.text()
            with open(file_path, mode='w') as file_writter: # type: ignore
                file_writter.write(data)



        if filePath == "":
            return
        self.canvas.save(filePath)
COMBINATIONS =[
     {keyboard.key.shift, keyboard.KeyCode(char='s') }]  [
         {keyboard.key.shift, keyboard.Keycode(char='a') }   ]
    

current = set()

def execute():
   print("Detected hotkey")
   
def on_press(key):
     if any([key in COMBO  for COMBO in COMBINATIONS]):
       current.add(key)
       if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
           execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
     current.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:listener.join()


    file_path = QFileDialog.str(title = "Custom Save Title",
                                             filetypes= type , initialdir=".")
    data = Entry.txt()  # type: ignore

    if file_path != "":
        file_writter = open(file_path, mode = 'w')
        file_writter.writter(data)
        file_writter.close()

