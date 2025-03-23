import sys
import os
import subprocess
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QProgressBar, QVBoxLayout, QDialog
from PyQt6.QtGui import QIcon, QPixmap, QCursor
from PyQt6.QtCore import QSize, Qt, QThread, pyqtSignal

# Define the folder and executable names, along with the correct GitHub Release download URLs
EXE_PATHS = {
    "icon1.png": ("GIMM1/GIMM1.exe", "Genshin Impact", "https://github.com/kxdekxde/GIMM1/releases/download/GIMM1/GIMM1.exe"),
    "icon2.png": ("SRMM1/SRMM1.exe", "Honkai: Star Rail", "https://github.com/kxdekxde/SRMM1/releases/download/SRMM1/SRMM1.exe"),
    "icon3.png": ("ZZZMM/ZZZMM.exe", "Zenless Zone Zero", "https://github.com/kxdekxde/ZZZMM/releases/download/ZZZMM/ZZZMM.exe"),
    "icon4.png": ("WWMM1/WWMM1.exe", "Wuthering Waves", "https://github.com/kxdekxde/WWMM1/releases/download/WWMM1/WWMM1.exe")
}

def resource_path(relative_path):
    """ Get the absolute path to the bundled resources. """
    if getattr(sys, 'frozen', False):  # If running as a bundled executable
        base_path = sys._MEIPASS  # This is the temp folder where PyInstaller stores the bundled files
    else:
        base_path = os.path.abspath(".")  # Regular development environment

    return os.path.join(base_path, relative_path)

class DownloadThread(QThread):
    download_progress = pyqtSignal(int)  
    download_finished = pyqtSignal(str, str)  # Emits the message and exe path

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0

            with open(self.save_path, 'wb') as f:
                for data in response.iter_content(chunk_size=1024):
                    if data:
                        f.write(data)
                        downloaded += len(data)
                        progress = int(100 * downloaded / total_size)
                        self.download_progress.emit(progress)  

            self.download_finished.emit("Download completed", self.save_path)
        except requests.RequestException as e:
            self.download_finished.emit(f"Error downloading file: {e}", "")

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Progress")
        self.setFixedSize(300, 100)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def download_finished(self, message):
        print(message)
        self.close()  

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

        icons = list(EXE_PATHS.keys())
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for i, (row, col) in enumerate(positions):
            button = QPushButton()
            icon_path = resource_path(icons[i])  # Updated icon path
            button.setIcon(QIcon(QPixmap(icon_path)))
            button.setIconSize(QSize(120, 120))
            button.setFixedSize(120, 120)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  
            button.setToolTip(EXE_PATHS[icons[i]][1])  
            button.clicked.connect(lambda checked, exe_path=EXE_PATHS[icons[i]][0], download_url=EXE_PATHS[icons[i]][2]: self.run_exe(exe_path, download_url))
            grid_layout.addWidget(button, row, col)

    def create_folders(self):
        for folder in ['GIMM1', 'SRMM1', 'ZZZMM', 'WWMM1']:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")

    def run_exe(self, exe_path, download_url):
        full_path = os.path.join(os.getcwd(), exe_path)
        exe_dir = os.path.dirname(full_path)  

        if not os.path.exists(full_path):  
            print(f"Executable not found in {exe_dir}, starting download from {download_url}...")
            self.start_download(download_url, full_path)
        else:
            subprocess.Popen(full_path, cwd=exe_dir)  

    def start_download(self, download_url, save_path):
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()

        self.download_thread = DownloadThread(download_url, save_path)
        self.download_thread.download_progress.connect(self.progress_dialog.update_progress)
        self.download_thread.download_finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self, message, exe_path):
        self.progress_dialog.download_finished(message)
        if message == "Download completed":
            self.run_exe_from_download(exe_path)  

    def run_exe_from_download(self, exe_path):
        exe_dir = os.path.dirname(exe_path)
        subprocess.Popen(exe_path, cwd=exe_dir)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageButtonApp()
    window.show()
    sys.exit(app.exec())
