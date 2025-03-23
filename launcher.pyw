import sys
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QCursor
from PyQt6.QtCore import QSize, Qt

# Define the folder and script names
SCRIPT_PATHS = {
    "icon1.png": ("GIMM1/GIMM1.pyw", "Genshin Impact"),
    "icon2.png": ("SRMM1/SRMM1.pyw", "Honkai: Star Rail"),
    "icon3.png": ("ZZZMM/ZZZMM.pyw", "Zenless Zone Zero"),
    "icon4.png": ("WWMM1/WWMM1.pyw", "Wuthering Waves")
}

def resource_path(relative_path):
    """ Get the absolute path to the bundled resources. """
    if getattr(sys, 'frozen', False):  # If running as a bundled executable
        base_path = sys._MEIPASS  # This is the temp folder where PyInstaller stores the bundled files
    else:
        base_path = os.path.abspath(".")  # Regular development environment

    return os.path.join(base_path, relative_path)

class ImageButtonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("XXMI Mods Manager")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: black;")  

        self.setWindowIcon(QIcon(resource_path("app_icon.png")))  # Updated icon path

        self.create_folders()

        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        icons = list(SCRIPT_PATHS.keys())
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for i, (row, col) in enumerate(positions):
            button = QPushButton()
            icon_path = resource_path(icons[i])  # Updated icon path
            button.setIcon(QIcon(QPixmap(icon_path)))
            button.setIconSize(QSize(120, 120))
            button.setFixedSize(120, 120)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  
            button.setToolTip(SCRIPT_PATHS[icons[i]][1])  
            button.clicked.connect(lambda checked, script_path=SCRIPT_PATHS[icons[i]][0]: self.run_script(script_path))
            grid_layout.addWidget(button, row, col)

    def create_folders(self):
        for folder in ['GIMM1', 'SRMM1', 'ZZZMM', 'WWMM1']:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")

    def run_script(self, script_path):
        full_path = os.path.join(os.getcwd(), script_path)
        script_dir = os.path.dirname(full_path)  

        if os.path.exists(full_path):  
            subprocess.Popen([sys.executable, full_path], cwd=script_dir)  
        else:
            print(f"Script not found in {script_dir}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageButtonApp()
    window.show()
    sys.exit(app.exec())