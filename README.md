# XXMI Mods Manager
A simple tool to manage [XXMI](https://github.com/SpectrumQT/XXMI-Launcher) mods folders.

With this tool you can activate/deactivate your mods. The tool basically renames the mod .ini file in a way that they appear disabled on XXMI, they can be activated/deactivated with the manager buttons like I show on my [video guide](https://files.catbox.moe/cqko1c.mp4).

If the mods you downloaded have got an .ini file that is already named with "DISABLED" you need to delete them or create an empty folder and move them inside, that way you can leave the main .ini file alone like the video (check the changes you're doing refreshing your mods on XXMI in real time to be sure the file you're deleting/moving is the correct one).
You can include your own "preview.jpg" image in your mod folder if the folder doesn't come with any preview image.
The launcher asks the user for the path to the mods folder the first time the mod manager is downloaded and launched, after that the user preferences should be saved so the next time the user uses the mod manager the last changes made should be still effective.
I show how to set the mod manager for Honkai: Star Rail but you can download and use the other ones for Genshin Impact/Zenless Zone Zero/Wuthering Waves as well, and you can use them separately.
After to activate/deactivate the mods you need, you can close the mod manager and the launcher if you want.


## Requirements before to use this tool

   - Install [Python](https://www.python.org/downloads/) (don't forget to mark 'pip' to be installed as well).
   - Install PyQt6 opening a CMD window and typing `pip install PyQt6`
   - Install PyInstaller with `pip install pyinstaller`

## Script version usage

1. Run *launcher.pyw* with double-click.
2. Click on the waifu image associated to the game/mod manager you want to use.
3. The mod manager will ask you for the mods folder path the first time the manager is launched, so you need to go to your XXMI mods folder location and to copy the path from the search bar.
4. Paste the path on the mod manager window and click OK, the mod manager will launch after that with all of your mods listed.

## Executable version usage

1. Download the [Launcher](https://gamebanana.com/dl/1402998) in some empty folder or go to your XXMI Launcher folder, create a new folder "XXMI Mods Manager" and move the Launcher there.
2. Run the launcher and click on the waifu image associated to the game/mod manager you want to download. The download will start.
3. After the download finishes the mod manager will ask you for the mods folder path the first time the manager is launched, so you need to go to your mods folder location and to copy the path from the search bar.
4. Paste the path on the mod manager window and click OK, the mod manager will launch after that with all of your mods listed.


## How to package it with PyInstaller (Executable version for launcher_online_downloads.pyw)

Open a CMD window in the folder location and input the next command:

```
pyinstaller --onefile --windowed --icon="app_icon.ico" --add-data "app_icon.png;." --add-data "icon1.png;." --add-data "icon2.png;." --add-data "icon3.png;." --add-data "icon4.png;." launcher_online_downloads.pyw
```


## Supported Model Importers Mods Folders

  - [GIMI](https://github.com/SilentNightSound/GI-Model-Importer)
  - [SRMI](https://github.com/SilentNightSound/SR-Model-Importer)
  - [ZZMI](https://github.com/leotorrez/ZZ-Model-Importer)
  - [WWMI](https://github.com/SpectrumQT/WWMI)
