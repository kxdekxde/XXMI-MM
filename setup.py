# setup.py
import sys
from cx_Freeze import setup, Executable
import os

# List of additional files to include
include_files = [
    "folder_1.png",
    "folder_2.png", 
    "folder_3.png",
    "folder_4.png",
    "icon.png"
]

# Dependencies
build_exe_options = {
    "packages": ["PyQt6", "os", "sys", "json", "platform", "subprocess"],
    "include_files": include_files,
    "excludes": ["tkinter"],
    "optimize": 2
}

# GUI application setup
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="XXMI Mods Manager",
    version="2.0",
    description="Mod Manager for XXMI Mods",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "XXMIMM.pyw",
            base=base,
            icon="icon.ico",
            target_name="XXMI_Mods_Manager.exe"
        )
    ]
)