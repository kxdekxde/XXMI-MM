import sys
import os
import json
import subprocess
import platform
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QScrollArea, QInputDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

SETTINGS_FILE = "mod_preferences.json"
MODS_FOLDER_FILE = "mods_folder_path.json"

class ModManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Honkai: Star Rail Mod Manager")
        self.setGeometry(100, 100, 700, 500)

        # Set window icon from bundled mod_icon.png
        self.setWindowIcon(QIcon(self.resource_path("mod_icon.png")))

        self.is_dark_mode = True
        self.apply_styles()

        self.mods_folder = self.get_mods_folder_path()
        self.checkbox_state = self.load_preferences()

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search mods...")
        self.search_bar.textChanged.connect(self.load_mods)
        left_layout.addWidget(self.search_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        left_layout.addWidget(self.scroll_area)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.activate_button = QPushButton("Activate Selected Mods")
        self.activate_button.clicked.connect(self.activate_mods)
        right_layout.addWidget(self.activate_button)

        self.deactivate_button = QPushButton("Deactivate Selected Mods")
        self.deactivate_button.clicked.connect(self.deactivate_mods)
        right_layout.addWidget(self.deactivate_button)

        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all_mods)
        right_layout.addWidget(self.select_all_button)

        self.Deselect_all_button = QPushButton("Deselect All")
        self.Deselect_all_button.clicked.connect(self.Deselect_all_mods)
        right_layout.addWidget(self.Deselect_all_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.load_mods)
        right_layout.addWidget(self.refresh_button)

        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)

        self.setLayout(main_layout)
        self.checkboxes = []

        self.load_mods()

    def apply_styles(self):
        """Apply dark mode styles."""
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E0E0E0;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #444444;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QScrollArea {
                background-color: #1E1E1E;
            }
        """)

    def resource_path(self, relative_path):
        """ Get the absolute path to a resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_mods_folder_path(self):
        """Get the custom mods folder path from JSON or prompt the user."""
        if os.path.exists(MODS_FOLDER_FILE):
            with open(MODS_FOLDER_FILE, "r") as file:
                return json.load(file)["mods_folder"]
        else:
            folder, ok = QInputDialog.getText(self, "Mods Folder Path", "Enter the path to the mods folder:")
            if ok and folder:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                with open(MODS_FOLDER_FILE, "w") as file:
                    json.dump({"mods_folder": folder}, file, indent=4)
                return folder
            else:
                sys.exit("No mods folder path provided, exiting.")

    def load_mods(self):
        """Loads mod folders, filters them, and maintains checkbox states."""
        search_text = self.search_bar.text().lower()
        self.clear_mod_list()

        for mod_folder in os.listdir(self.mods_folder):
            if mod_folder == "BufferValues":
                continue

            mod_path = os.path.join(self.mods_folder, mod_folder)
            if os.path.isdir(mod_path):
                ini_files = [f for f in os.listdir(mod_path) if f.endswith(".ini")]
                if ini_files:
                    ini_file = ini_files[0]

                    if search_text and search_text not in mod_folder.lower():
                        continue

                    mod_row_layout = QHBoxLayout()

                    checkbox = QCheckBox(mod_folder)
                    is_active = not ini_file.startswith("DISABLED")

                    checkbox.setChecked(self.checkbox_state.get(mod_folder, is_active))

                    if is_active:
                        checkbox.setStyleSheet("QCheckBox { color: green; }")
                    else:
                        checkbox.setStyleSheet("QCheckBox { color: red; }")

                    checkbox.stateChanged.connect(self.save_checkbox_state)

                    # Preview button with fixed width
                    preview_button = QPushButton("Preview")
                    preview_button.setFixedWidth(100)  # Set the fixed width for the Preview button
                    preview_button.clicked.connect(lambda _, mod_folder=mod_folder: self.preview_mod(mod_folder))

                    mod_row_layout.addWidget(preview_button)
                    mod_row_layout.addWidget(checkbox)

                    self.scroll_layout.addLayout(mod_row_layout)
                    self.checkboxes.append((checkbox, mod_folder, ini_file))

    def rename_ini_file(self, mod_folder, ini_file, activate):
        """Renames the .ini file to activate or deactivate the mod."""
        mod_path = os.path.join(self.mods_folder, mod_folder, ini_file)

        if activate:
            if ini_file.startswith("DISABLED"):
                new_name = ini_file.replace("DISABLED", "", 1)
                os.rename(mod_path, os.path.join(self.mods_folder, mod_folder, new_name))
        else:
            if not ini_file.startswith("DISABLED"):
                new_name = f"DISABLED{ini_file}"
                os.rename(mod_path, os.path.join(self.mods_folder, mod_folder, new_name))

    def activate_mods(self):
        """Activates selected mods and Deselects the checkboxes."""
        for checkbox, mod_folder, ini_file in self.checkboxes:
            if checkbox.isChecked():
                self.rename_ini_file(mod_folder, ini_file, activate=True)
                checkbox.setChecked(False)  # Deselect after activation
        self.save_preferences()
        self.load_mods()

    def deactivate_mods(self):
        """Deactivates selected mods and Deselects the checkboxes."""
        for checkbox, mod_folder, ini_file in self.checkboxes:
            if checkbox.isChecked():
                self.rename_ini_file(mod_folder, ini_file, activate=False)
                checkbox.setChecked(False)  # Deselect after deactivation
        self.save_preferences()
        self.load_mods()

    def select_all_mods(self):
        """Selects all mods."""
        for checkbox, _, _ in self.checkboxes:
            checkbox.setChecked(True)

    def Deselect_all_mods(self):
        """Deselects all mods."""
        for checkbox, _, _ in self.checkboxes:
            checkbox.setChecked(False)

    def save_checkbox_state(self):
        """Saves checkbox states in real-time."""
        for checkbox, mod_folder, _ in self.checkboxes:
            self.checkbox_state[mod_folder] = checkbox.isChecked()
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.checkbox_state, file, indent=4)

    def save_preferences(self):
        """Saves the preferences."""
        preferences = {mod_folder: checkbox.isChecked() for checkbox, mod_folder, _ in self.checkboxes}
        with open(SETTINGS_FILE, "w") as file:
            json.dump(preferences, file, indent=4)

    def load_preferences(self):
        """Loads mod preferences."""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        return {}

    def clear_mod_list(self):
        """Clears the mod list."""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.checkboxes = []

    def preview_mod(self, mod_folder):
        """Opens the preview image for the mod."""
        preview_image = os.path.join(self.mods_folder, mod_folder, "preview.jpg")
        
        # Check if the preview image exists
        if os.path.exists(preview_image):
            try:
                # Open image using appropriate method based on the OS
                if platform.system() == "Windows":
                    os.startfile(preview_image)  # Windows: opens file with associated program
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", preview_image], check=True)
                else:  # Linux
                    subprocess.run(["xdg-open", preview_image], check=True)
            except Exception as e:
                print(f"Error opening preview: {e}")
        else:
            print(f"Preview image for {mod_folder} not found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModManager()
    window.show()
    sys.exit(app.exec())
