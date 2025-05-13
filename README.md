# XXMI Mods Manager

![XXMI Mods Manager](https://files.catbox.moe/a1xrpe.png)

![XXMI Mods Manager](https://files.catbox.moe/kv2dzs.png)


A simple tool to manage [XXMI](https://github.com/SpectrumQT/XXMI-Launcher) mods folders.

With this tool you can activate/deactivate your mods. The tool basically renames the mod .ini file in a way that they appear disabled on XXMI, they can be activated/deactivated with the manager buttons like I show on my [video guide](https://files.catbox.moe/cqko1c.mp4).

If the mods you downloaded have got an .ini file that is already named with "DISABLED" you need to delete them or create an empty folder and move them there, that way you can leave the main .ini file alone like the video (check the changes you're doing refreshing your mods on XXMI in real time to be sure the file you're deleting/moving is the correct one).
You can include your own "preview.jpg" image in your mod folder if the folder doesn't come with any preview image.
The user needs to set the paths to their mods folders the first time the manager is launched, after that the user preferences will be saved so the next time the mod manager is launched the last changes made should be still effective.
I show how to set the mod manager for Honkai: Star Rail but the process is the same for Genshin Impact/Zenless Zone Zero/Wuthering Waves as well.
After to activate/deactivate the mods you need, you can close the mod manager if you want.


## Requirements to run the scripts

   - Double click on _install_requirements.bat_ to install the required dependencies and Python 3.13.


## Script version usage

1. Run *XXMIMM.pyw* with double-click.
2. Click on the button `Browse...`, navigate to your "mods" folder and select it.
3. Click on the waifu image associated to the game to see the respective mods list from that mods folder.
4. If the mods contain a *preview.jpg* image in the folder the Mods Manager will be able to open it with the button `Preview`. 

## Executable version usage

1. Download the executable from [here](https://www.mediafire.com/file/jyyj10cyxcwiig3/XXMI_Mods_Manager.7z/file) in some empty folder or go to your XXMI Launcher folder, create a new folder "XXMI Mods Manager", move the downloaded file there and extract the content.
2. Run the executable _XXMI_Mods_Manager.exe_ with double-click. 
3. Click on the button `Browse...`, navigate to your "mods" folder and select it.
4. Click on the waifu image associated to the game to see the respective mods list from that mods folder.
5. If the mods contain a *preview.jpg* image in the folder the Mods Manager will be able to open it with the button `Preview`. 


## How to build it with cxFreeze (Executable version)

Open a CMD window in the folder location and input the next command:

```
python setup.py build
```
### NOTE: The command above is for the version _`XXMIMM_forbuild.pyw`_ that is for the executable.


## Supported Model Importers Mods Folders

  - [GI-Model-Importer](https://github.com/SilentNightSound/GI-Model-Importer)
  - [SR-Model-Importer](https://github.com/SilentNightSound/SR-Model-Importer)
  - [ZZ-Model-Importer](https://github.com/leotorrez/ZZ-Model-Importer)
  - [WWMI-Package](https://github.com/SpectrumQT/WWMI)
