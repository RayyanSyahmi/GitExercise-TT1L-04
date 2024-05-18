import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QStackedWidget
from PyQt5.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.active_tool = None

    def initUI(self):
        self.setWindowTitle("Drawing app")
        self.setGeometry(150, 150, 650, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        central_widget.setLayout(main_layout)

        self.sidebar_layout = QVBoxLayout()
        main_layout.addLayout(self.sidebar_layout)

        tool_label = QLabel("Tools")
        self.sidebar_layout.addWidget(tool_label)
        self.sidebar_layout.addStretch(1)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))

        brushicon = os.path.join(script_dir, 'icons', 'brushicon.png')
        erasericon = os.path.join(script_dir, 'icons', 'erasericon.png')
        undoicon = os.path.join(script_dir, 'icons', 'undoicon.png')
        redoicon = os.path.join(script_dir, 'icons', 'redoicon.png')

        print(f"Brush icon path: {brushicon}, Exists: {os.path.exists(brushicon)}")
        print(f"Eraser icon path: {erasericon}, Exists: {os.path.exists(erasericon)}")
        print(f"Undo icon path: {undoicon}, Exists: {os.path.exists(undoicon)}")
        print(f"Redo icon path: {redoicon}, Exists: {os.path.exists(redoicon)}")

        self.brush_button = QPushButton('')
        self.brush_button.setToolTip('Select The Brush tool')
        self.brush_button.setFixedHeight(30)
        self.brush_button.setFixedWidth(80)
        self.brush_button.setIcon(QIcon(brushicon))  
        self.brush_button.clicked.connect(lambda: self.set_active_tool("Brush"))

        self.eraser_button = QPushButton('')
        self.eraser_button.setToolTip('Select The Eraser Tool')
        self.eraser_button.setFixedHeight(30)
        self.eraser_button.setFixedWidth(80)
        self.eraser_button.setIcon(QIcon(erasericon))  
        self.eraser_button.clicked.connect(lambda: self.set_active_tool("Eraser"))

        self.sidebar_layout.addWidget(self.brush_button)
        self.sidebar_layout.addWidget(self.eraser_button)
        self.sidebar_layout.setAlignment(self.brush_button, Qt.AlignTop)
        self.sidebar_layout.setAlignment(self.eraser_button, Qt.AlignTop)

        self.stacked_widget = QStackedWidget()
        self.sidebar_layout.addWidget(self.stacked_widget)

        brush_settings_widget = QWidget()
        brush_settings_layout = QVBoxLayout()
        brush_settings_widget.setLayout(brush_settings_layout)

        self.brush_thickness_label = QLabel("Thickness: 5")
        brush_settings_layout.addWidget(self.brush_thickness_label)

        thickness_slider = QSlider()
        thickness_slider.setOrientation(Qt.Horizontal)
        thickness_slider.setMinimum(1)
        thickness_slider.setMaximum(100)
        thickness_slider.setValue(5)
        thickness_slider.valueChanged.connect(lambda value, label=self.brush_thickness_label: self.update_thickness_label(value, label))
        brush_settings_layout.addWidget(thickness_slider)

        self.brush_size_label = QLabel("Size: 5")
        brush_settings_layout.addWidget(self.brush_size_label)

        size_slider = QSlider()
        size_slider.setOrientation(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(lambda value, label=self.brush_size_label: self.update_slider_label(value, label))
        brush_settings_layout.addWidget(size_slider)

        self.stacked_widget.addWidget(brush_settings_widget)

        eraser_settings_widget = QWidget()
        eraser_settings_layout = QVBoxLayout()
        eraser_settings_widget.setLayout(eraser_settings_layout)

        self.eraser_size_label = QLabel("Size: 5")
        eraser_settings_layout.addWidget(self.eraser_size_label)

        eraser_size_slider = QSlider()
        eraser_size_slider.setOrientation(Qt.Horizontal)
        eraser_size_slider.setMinimum(1)
        eraser_size_slider.setMaximum(100)
        eraser_size_slider.setValue(5)
        eraser_size_slider.valueChanged.connect(lambda value, label=self.eraser_size_label: self.update_slider_label(value, label))
        eraser_settings_layout.addWidget(eraser_size_slider)

        self.stacked_widget.addWidget(eraser_settings_widget)

        self.stacked_widget.setCurrentWidget(brush_settings_widget)

        main_layout.addStretch(1)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        undo_action = QAction(QIcon(undoicon), 'Undo', self)
        redo_action = QAction(QIcon(redoicon), 'Redo', self)

        menubar.addAction(undo_action)
        menubar.addAction(redo_action)
       
        brush_settings_widget.hide()
        eraser_settings_widget.hide()

    def save(self):
        print("Save action triggered!")

    def show_brush_settings(self):
        self.stacked_widget.setCurrentIndex(0)  
        self.stacked_widget.currentWidget().show()  

    def show_eraser_settings(self):
        self.stacked_widget.setCurrentIndex(1)  
        self.stacked_widget.currentWidget().show()  

    def update_slider_label(self, value, label):
        label.setText(f"Size: {value}")
    
    def update_thickness_label(self, value, label):
        label.setText(f"Thickness: {value}")

    def set_active_tool(self, tool_name):
        if self.active_tool == tool_name:
            self.active_tool = None
            self.stacked_widget.currentWidget().hide()
        else:
            self.active_tool = tool_name
            if tool_name == "Brush":
                self.stacked_widget.setCurrentIndex(0)
            else:
                self.stacked_widget.setCurrentIndex(1)

            self.stacked_widget.currentWidget().show()

        if self.active_tool == "Brush":
            self.brush_button.setStyleSheet("background-color: #2196F3; color: white;")
            self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        elif self.active_tool == "Eraser":
            self.eraser_button.setStyleSheet("background-color: #2196F3; color: white;")
            self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        else:
            self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")
            self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    app.setStyleSheet("QPushButton{ font-family: 'Segoe UI'; font-size: 9pt; }")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())