import sys
from PyQt5.QtWidgets import QFileDialog 
import keyboard  # type: ignore

def save_file():
    types = [ ("Text Files", "*.txt"),
              ("All Files", "*.*"),
              ("Png Files", "*.png"),
              ("Jpeg Files", "*.jpg *.jpeg")]

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
