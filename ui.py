import sys
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QApplication, QInputDialog, QAction, QColorDialog, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QLabel, QSlider

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
        central_widget.setLayout(main_layout)

        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #f0f0f0;")
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        main_layout.addWidget(self.sidebar)

        tool_label = QLabel("Tools")
        self.sidebar_layout.addWidget(tool_label)

        self.brush_button = QPushButton('Brush')
        self.brush_button.setToolTip('Select The Brush tool')
        self.brush_button.setFixedHeight(30)
        self.brush_button.setFixedWidth(80)
        self.brush_button.clicked.connect(lambda: self.set_active_tool("Brush"))  
        self.brush_button.clicked.connect(self.show_brush_settings)  
        self.sidebar_layout.addWidget(self.brush_button)
        
        self.brush_settings_widget = QWidget()
        brush_settings_layout = QVBoxLayout()
        self.brush_settings_widget.setLayout(brush_settings_layout)

        self.brush_thickness_label = QLabel("Thickness: 5")
        brush_settings_layout.addWidget(self.brush_thickness_label)

        thickness_slider = QSlider()
        thickness_slider.setOrientation(1)
        thickness_slider.setMinimum(1)
        thickness_slider.setMaximum(100)
        thickness_slider.setValue(5)
        thickness_slider.valueChanged.connect(lambda value, label=self.brush_thickness_label: self.update_thickness_label(value, label))
        brush_settings_layout.addWidget(thickness_slider)

        self.brush_size_label = QLabel("Size: 5")
        brush_settings_layout.addWidget(self.brush_size_label)

        size_slider = QSlider()   
        size_slider.setOrientation(1)
        size_slider.setMinimum(1)
        size_slider.setMaximum(100)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(lambda value, label = self.brush_size_label: self.update_slider_label(value, label))
        brush_settings_layout.addWidget(size_slider)

        self.brush_settings_widget.hide()
        self.sidebar_layout.addWidget(self.brush_settings_widget)

        self.eraser_button = QPushButton('Eraser')
        self.eraser_button.setToolTip('Select The Eraser Tool')
        self.eraser_button.setFixedHeight(30)
        self.eraser_button.setFixedWidth(80)
        self. eraser_button.clicked.connect(self.show_eraser_settings)
        self.sidebar_layout.addWidget(self.eraser_button)
        self.eraser_button.clicked.connect(lambda: self.set_active_tool("Eraser"))

        self.eraser_settings_widget = QWidget()
        eraser_settings_layout = QVBoxLayout()
        self.eraser_settings_widget.setLayout(eraser_settings_layout)

        self.eraser_size_label = QLabel("Size: 5")
        eraser_settings_layout.addWidget(self.eraser_size_label)
 
        eraser_size_slider = QSlider()
        eraser_size_slider.setOrientation(1)
        eraser_size_slider.setMinimum(1)
        eraser_size_slider.setMaximum(100)
        eraser_size_slider.setValue(5)
        eraser_size_slider.valueChanged.connect(lambda value: self.update_slider_label(value, self.eraser_size_label))
        eraser_settings_layout.addWidget(eraser_size_slider)

        self.eraser_settings_widget.hide()
        self.sidebar_layout.addWidget(self.eraser_settings_widget)

        main_layout.addStretch(1)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        size_action = QAction('Size', self)
        size_action.triggered.connect(self.change_size)
        file_menu.addAction(size_action)

        color_action = QAction('Color', self)
        color_action.triggered.connect(self.change_color)
        file_menu.addAction(color_action)

        file_menu.addAction(save_action)

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

    def toggle_tool_settings(self):
        self.brush_button.setVisible(not self.brush_button.isVisible())
        self.eraser_button.setVisible(not self.eraser_button.isVisible())

    def show_brush_settings(self):
        if self.brush_settings_widget.isHidden():
            self.brush_settings_widget.show()
        else:
            self.brush_settings_widget.hide()
    
    def show_eraser_settings(self):
        if self.eraser_settings_widget.isHidden():
            self.eraser_settings_widget.show()
        else:
            self.eraser_settings_widget.hide()

    def update_slider_label(self, value, label):
        label.setText(f"Size: {value}")
    
    def update_thickness_label(self, value, label):
        label.setText(f"Thickness: {value}")

    def set_active_tool(self, tool_name):
        self.active_tool = tool_name

        if tool_name == "Brush":
            self.brush_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.eraser_button.setStyleSheet("background-color: #f0f0f0; color: black;")
        elif tool_name == "Eraser":
            self.eraser_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.brush_button.setStyleSheet("background-color: #f0f0f0; color: black;")


            self.brush_button.setStyle(QApplication.style())
            self.eraser_button.setStyle(QApplication.style())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QPushButton{ font-size: 14px; }")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
