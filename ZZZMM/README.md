# Zenless Zone Zero Mod Manager
A simple tool to manage [XXMI](https://github.com/SpectrumQT/XXMI-Launcher) mods folder.

With this tool you can activate/deactivate your mods. The tool basically renames the mod .ini file in a way that they appear disabled on XXMI, they can be activated/deactivated with the manager buttons like I show on my [video guide](https://files.catbox.moe/cqko1c.mp4).

If the mods you downloaded have got an .ini file that is already named with "DISABLED" you need to delete them or create an empty folder and move them inside, that way you can leave the main .ini file alone like the video (check the changes you're doing refreshing your mods on XXMI in real time to be sure the file you're deleting/moving is the correct one).
You can include your own "preview.jpg" image in your mod folder if the folder doesn't come with any preview image.
The launcher asks the user for the path to the mods folder the first time the mod manager is downloaded and launched, after that the user preferences should be saved so the next time the user uses the mod manager the last changes made should be still effective.
I show how to set the mod manager for Honkai: Star Rail but you can download and use the other ones for Genshin Impact/Zenless Zone Zero/Wuthering Waves as well, and you can use them separately.
After to activate/deactivate the mods you need, you can close the mod manager and the launcher if you want.


## Requirements before to use this tool

   - Install [Python](https://www.python.org/downloads/) (don't forget to mark 'pip' to be installed as well).
   - Install PyQt6 opening a CMD window and typing 
   ```
   pip install PyQt6
   ```
   - Install PyInstaller
   ```
   pip install pyinstaller
   ```


## Script Usage

1. Run *ZZZMM.pyw* with double-click, the first time you will need to set the path to your ZZMI/XXMI mods folder.
2. Go to your ZZMI/XXMI mods folder and copy the path from your search bar.
3. Paste the path on the manager window and click OK.
4. The mod manager will be launched showing a list with your mods, and the script will create two new JSON files `mod_preferences.json` and `mods_folder_path.json` in ZZZMM folder to save the user preferences.


## How to package it with PyInstaller (Executable version)

Open a CMD window in the folder location and input the next command:

```
pyinstaller --onefile --windowed --icon="ZZZMM.ico" --add-data "mod_icon.png;." --add-data "mods_folder_path.json;." --add-data "mod_preferences.json;." ZZZMM.pyw
```

