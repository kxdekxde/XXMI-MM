import sys
import os
import json
import subprocess
import platform
import ctypes
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox,
                            QLineEdit, QHBoxLayout, QScrollArea, QLabel,
                            QMessageBox, QFileDialog, QGridLayout)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# Constants for Windows dark mode
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

SETTINGS_FILE = "mod_preferences.json"
MODS_FOLDER_FILE = "mods_folder_paths.json"

class ModManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XXMI Mods Manager")
        self.setGeometry(100, 100, 1100, 600)
        self.setWindowIcon(QIcon(self.resource_path("icon.png")))
        self.is_dark_mode = True

        # Initialize mod folders
        self.mods_folders = self.load_mods_folder_paths()
        self.current_mods_folder_index = 0
        self.current_mods_folder = self.mods_folders[self.current_mods_folder_index] if self.mods_folders else ""
        self.checkbox_state = self.load_preferences()

        # Game-specific configuration
        self.game_config = [
            {"name": "Genshin Impact mods folder", "abbr": "GI"},
            {"name": "Honkai: Star Rail mods folder", "abbr": "HSR"},
            {"name": "Zenless Zone Zero mods folder", "abbr": "ZZZ"},
            {"name": "Wuthering Waves mods folder", "abbr": "WW"}
        ]

        # Main layout using grid
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Left column (search bars and mod list)
        left_column = QVBoxLayout()
        
        # SEARCH BARS (vertical)
        search_bars_layout = QVBoxLayout()
        self.search_bars = []
        for i in range(4):
            # Container for search bar + browse button
            search_row = QHBoxLayout()
            
            # Search bar with custom game name
            search_bar = QLineEdit()
            search_bar.setPlaceholderText(self.game_config[i]["name"])
            search_bar.setText(self.mods_folders[i] if i < len(self.mods_folders) else "")
            search_bar.textChanged.connect(lambda text, idx=i: self.update_mods_folder_path(idx, text))
            self.search_bars.append(search_bar)
            search_row.addWidget(search_bar, stretch=4)
            
            # Browse button
            browse_btn = QPushButton("Browse...")
            browse_btn.setFixedWidth(80)
            browse_btn.clicked.connect(lambda _, idx=i: self.browse_for_folder(idx))
            search_row.addWidget(browse_btn)
            
            search_bars_layout.addLayout(search_row)
        
        left_column.addLayout(search_bars_layout)

        # IMAGE BUTTONS (horizontal below search bars)
        buttons_layout = QHBoxLayout()
        self.folder_buttons = []
        for i in range(4):
            btn = QPushButton()
            btn.setFixedSize(100, 100)
            btn.setIconSize(QSize(90, 90))
            
            # Try to load icon or use game abbreviation
            icon_path = self.resource_path(f"folder_{i+1}.png")
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
            else:
                btn.setText(self.game_config[i]["abbr"])
                btn.setStyleSheet("font-size: 14px; font-weight: bold;")
                
            btn.clicked.connect(lambda _, idx=i: self.switch_mods_folder(idx))
            self.folder_buttons.append(btn)
            buttons_layout.addWidget(btn)
        
        left_column.addLayout(buttons_layout)

        # Current folder label
        self.current_folder_label = QLabel("Current Folder: " + (self.current_mods_folder if self.current_mods_folder else "None"))
        left_column.addWidget(self.current_folder_label)

        # Container for mod list and action buttons
        content_row = QHBoxLayout()
        
        # Mod list scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        content_row.addWidget(self.scroll_area, stretch=4)

        # Right side controls (vertical layout)
        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Control buttons
        self.activate_btn = QPushButton("Activate Selected")
        self.activate_btn.clicked.connect(self.activate_mods)
        right_side.addWidget(self.activate_btn)
        
        self.deactivate_btn = QPushButton("Deactivate Selected")
        self.deactivate_btn.clicked.connect(self.deactivate_mods)
        right_side.addWidget(self.deactivate_btn)
        
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_mods)
        right_side.addWidget(self.select_all_btn)
        
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_mods)
        right_side.addWidget(self.deselect_all_btn)
        
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.load_mods)
        right_side.addWidget(self.refresh_btn)
        
        right_side.addStretch()
        content_row.addLayout(right_side, stretch=1)
        left_column.addLayout(content_row)

        main_layout.addLayout(left_column, 0, 0)

        self.checkboxes = []
        self.load_mods()
        self.apply_styles()
        self.set_win_dark_title_bar()

    def set_win_dark_title_bar(self):
        """Set dark mode for Windows title bar."""
        if platform.system() == "Windows":
            try:
                hwnd = self.winId().__int__()
                if hwnd:
                    dwmapi = ctypes.windll.dwmapi
                    value = ctypes.c_int(1)
                    # Try both versions of the API
                    for attribute in [DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1, DWMWA_USE_IMMERSIVE_DARK_MODE]:
                        result = dwmapi.DwmSetWindowAttribute(
                            hwnd,
                            attribute,
                            ctypes.byref(value),
                            ctypes.sizeof(value)
                        )
                        if result == 0:  # Success
                            break
            except Exception as e:
                print(f"Error setting dark title bar: {e}")

    def resource_path(self, relative_path):
        """Get absolute path to resource."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def apply_styles(self):
        """Apply Windows 11 dark mode styles with dark message boxes."""
        self.setStyleSheet("""
            /* Main window and general widgets */
            QWidget {
                background-color: #202020;
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 9pt;
                border: none;
            }
            
            /* Text input fields */
            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
                padding: 5px 8px;
                selection-background-color: #0078D4;
            }
            QLineEdit:hover {
                border-color: #505050;
            }
            QLineEdit:focus {
                border-color: #0078D4;
            }
            
            /* Buttons */
            QPushButton {
                background-color: #3D3D3D;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
                padding: 5px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4D4D4D;
                border-color: #4D4D4D;
            }
            QPushButton:pressed {
                background-color: #2D2D2D;
                border-color: #2D2D2D;
            }
            QPushButton:disabled {
                color: #6D6D6D;
            }
            
            /* Scroll area */
            QScrollArea {
                background-color: #1E1E1E;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
            }
            
            /* Enhanced Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: #1E1E1E;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4D4D4D;
                min-height: 20px;
                border-radius: 6px;
                border: 2px solid #1E1E1E;
            }
            QScrollBar::handle:vertical:hover {
                background: #5E5E5E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            /* Checkboxes */
            QCheckBox {
                spacing: 8px;
                color: #FFFFFF;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #5E5E5E;
                border-radius: 4px;
                background-color: #2D2D2D;
            }
            QCheckBox::indicator:hover {
                background-color: #3D3D3D;
            }
            QCheckBox::indicator:checked {
                background-color: #0078D4;
                border-color: #0078D4;
            }
            
            /* Labels */
            QLabel {
                color: #FFFFFF;
                padding: 2px;
            }
            
            /* Active/Inactive mod indicators */
            QCheckBox[activeMod="true"] {
                color: #4CAF50;
            }
            QCheckBox[inactiveMod="true"] {
                color: #F44336;
            }
            
            /* Game folder buttons */
            QPushButton[folderButton="true"] {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
            }
            QPushButton[folderButton="true"]:hover {
                background-color: #3D3D3D;
            }
            
            /* Message Box Styling */
            QMessageBox {
                background-color: #202020;
                color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
            }
            QMessageBox QPushButton {
                background-color: #3D3D3D;
                color: #FFFFFF;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
                padding: 5px 12px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4D4D4D;
                border-color: #4D4D4D;
            }
            QMessageBox QPushButton:pressed {
                background-color: #2D2D2D;
                border-color: #2D2D2D;
            }
        """)
        
        for btn in self.folder_buttons:
            btn.setProperty("folderButton", "true")

    def browse_for_folder(self, index):
        """Open folder dialog to select mods folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            f"Select {self.game_config[index]['name']}",
            os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            self.search_bars[index].setText(folder)
            self.update_mods_folder_path(index, folder)

    def update_mods_folder_path(self, index, path):
        """Update the path for a specific mod folder."""
        if index < len(self.mods_folders):
            self.mods_folders[index] = path.strip()
            self.save_mods_folder_paths()
            
            if index == self.current_mods_folder_index:
                self.current_mods_folder = path.strip()
                self.current_folder_label.setText(f"Current Folder: {self.game_config[index]['name']}\n{self.current_mods_folder}")
                self.load_mods()

    def switch_mods_folder(self, index):
        """Switch to a different mod folder."""
        if index < len(self.mods_folders) and self.mods_folders[index]:
            self.current_mods_folder_index = index
            self.current_mods_folder = self.mods_folders[index]
            self.current_folder_label.setText(f"Current Folder: {self.game_config[index]['name']}\n{self.current_mods_folder}")
            self.load_mods()

    def load_mods_folder_paths(self):
        """Load saved mod folder paths."""
        if os.path.exists(MODS_FOLDER_FILE):
            with open(MODS_FOLDER_FILE, "r") as f:
                data = json.load(f)
                return data.get("mods_folders", ["", "", "", ""])
        return ["", "", "", ""]

    def save_mods_folder_paths(self):
        """Save current mod folder paths."""
        with open(MODS_FOLDER_FILE, "w") as f:
            json.dump({"mods_folders": self.mods_folders}, f, indent=4)

    def load_mods(self):
        """Load mods from current folder."""
        self.clear_mod_list()
        
        if not self.current_mods_folder or not os.path.exists(self.current_mods_folder):
            return

        for mod_folder in os.listdir(self.current_mods_folder):
            if mod_folder == "BufferValues":
                continue

            mod_path = os.path.join(self.current_mods_folder, mod_folder)
            if os.path.isdir(mod_path):
                ini_files = [f for f in os.listdir(mod_path) if f.endswith(".ini")]
                if ini_files:
                    ini_file = ini_files[0]

                    mod_row = QHBoxLayout()
                    
                    # Preview button
                    preview_btn = QPushButton("Preview")
                    preview_btn.setFixedWidth(80)
                    preview_btn.clicked.connect(lambda _, m=mod_folder: self.preview_mod(m))
                    mod_row.addWidget(preview_btn)
                    
                    # Checkbox
                    checkbox = QCheckBox(mod_folder)
                    is_active = not ini_file.startswith("DISABLED")
                    checkbox.setChecked(self.checkbox_state.get(f"{self.current_mods_folder}|{mod_folder}", is_active))
                    checkbox.setProperty("activeMod", "true" if is_active else "false")
                    checkbox.setProperty("inactiveMod", "false" if is_active else "true")
                    checkbox.stateChanged.connect(self.save_checkbox_state)
                    mod_row.addWidget(checkbox)
                    
                    self.scroll_layout.addLayout(mod_row)
                    self.checkboxes.append((checkbox, mod_folder, ini_file))

    def clear_mod_list(self):
        """Clear the current mod list."""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.checkboxes = []

    def save_checkbox_state(self):
        """Save checkbox states with folder context."""
        for checkbox, mod_folder, _ in self.checkboxes:
            key = f"{self.current_mods_folder}|{mod_folder}"
            self.checkbox_state[key] = checkbox.isChecked()
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.checkbox_state, f, indent=4)

    def load_preferences(self):
        """Load saved preferences."""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def activate_mods(self):
        """Activate selected mods."""
        for checkbox, mod_folder, ini_file in self.checkboxes:
            if checkbox.isChecked():
                self.rename_ini_file(mod_folder, ini_file, True)
        self.load_mods()

    def deactivate_mods(self):
        """Deactivate selected mods."""
        for checkbox, mod_folder, ini_file in self.checkboxes:
            if checkbox.isChecked():
                self.rename_ini_file(mod_folder, ini_file, False)
        self.load_mods()

    def rename_ini_file(self, mod_folder, ini_file, activate):
        """Rename .ini file to activate/deactivate mod."""
        mod_path = os.path.join(self.current_mods_folder, mod_folder, ini_file)
        
        if activate:
            if ini_file.startswith("DISABLED"):
                new_name = ini_file.replace("DISABLED", "", 1)
                os.rename(mod_path, os.path.join(self.current_mods_folder, mod_folder, new_name))
        else:
            if not ini_file.startswith("DISABLED"):
                new_name = f"DISABLED{ini_file}"
                os.rename(mod_path, os.path.join(self.current_mods_folder, mod_folder, new_name))

    def select_all_mods(self):
        """Select all mod checkboxes."""
        for checkbox, _, _ in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all_mods(self):
        """Deselect all mod checkboxes."""
        for checkbox, _, _ in self.checkboxes:
            checkbox.setChecked(False)

    def preview_mod(self, mod_folder):
        """Open preview image for mod."""
        preview_path = os.path.join(self.current_mods_folder, mod_folder, "preview.jpg")
        if os.path.exists(preview_path):
            try:
                if platform.system() == "Windows":
                    os.startfile(preview_path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", preview_path], check=True)
                else:
                    subprocess.run(["xdg-open", preview_path], check=True)
            except Exception as e:
                # Create styled error message box
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"Couldn't open preview:\n{e}")
                msg.setStyleSheet(self.styleSheet())
                self.set_win_dark_title_bar_for_dialog(msg)
                msg.exec()
        else:
            # Create styled information message box
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("No Preview")
            msg.setText(f"No preview image found for {mod_folder}")
            msg.setStyleSheet(self.styleSheet())
            self.set_win_dark_title_bar_for_dialog(msg)
            msg.exec()

    def set_win_dark_title_bar_for_dialog(self, dialog):
        """Set dark mode for Windows title bar on dialogs."""
        if platform.system() == "Windows":
            try:
                hwnd = dialog.winId().__int__()
                if hwnd:
                    dwmapi = ctypes.windll.dwmapi
                    value = ctypes.c_int(1)
                    # Try both versions of the API
                    for attribute in [DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1, DWMWA_USE_IMMERSIVE_DARK_MODE]:
                        result = dwmapi.DwmSetWindowAttribute(
                            hwnd,
                            attribute,
                            ctypes.byref(value),
                            ctypes.sizeof(value)
                        )
                        if result == 0:  # Success
                            break
            except Exception as e:
                print(f"Error setting dark title bar on dialog: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ModManager()
    manager.show()
    sys.exit(app.exec())