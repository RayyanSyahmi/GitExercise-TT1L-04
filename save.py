import sys
from PyQt5.QtWidgets import QFileDialog

def save_file():
    types = [ ("Text Files", "*.txt"),
              ("All Files", "*.*"),
              ("Png Files", "*.png"),
              ("Jpeg Files", "*.jpg *.jpeg")]

    file_path = QFileDialog.asksavesfilename(title = "Custom Save Title",
                                             filetypes= types, initialdir=".")
    data = entry.get()

    if file_path != "":
        file_writter = open(file_path, mode = 'W')
        file_writter.writter(data)
        file_writter.close()
    