# My File Manager
## Description:
    MyFMTk is a minimal file manager.
    Designed for quick navigation through the list of text, photo and video files.
    After starting the program, double-click on the window header, expand MyFMTk to full screen.

## Software requirements:
    The application requires `python3` to run.
    Run the following command to install the required dependencies:
    for Debian, Ubuntu:
    `sudo apt install python3-tk python3-magic python3-pil python3-pil.imagetk`

    for OpenSuse:
    `sudo zypper install python3-tk python3-python-magic python3-Pillow python3-Pillow-tk`
    To clear X resources, type in the console:
    `xrdb -load / dev / null`
    `xrdb -query`
    If python3-magic is installed:
    `sudo zypper remove python3-magic`
    `sudo zypper install python3-python-magic`

## Features of the file list:
    names of text, photo and media files are highlighted with a colored background,
    all other files have a white background.
    The name of the selected file is duplicated in the bottom line of the FM window.
    If it is a link, then the full path of the link and the full real path are indicated.

## Basic mouse button controls:
    1. Double click on the name of the "File Manager" window:
        FM will expand to full screen and a window will open on the right,
        to view the contents of text files
    2. Double click on the folder address bar:
        a menu for selecting a new folder for work will open
    3. Double click on the name "..."
        go to parent folder
    4. Double click on the folder name:
        go to this folder
    5. Double click on the file name, the file will be launched by the default application
       Following the link is prohibited, so there is no action
    6. Single click on the name of the text file or image (only in full screen mode):
        view file content
        (you can move through the list of files using the up and down arrow keys)
    7. Click the Right mouse button on the address bar - call the folder open menu
    8. Right-click on the file list field - open the file management menu

## Sorting files:
    1. Single click on the column name:
        files are sorted according to the name of this column
    2. Click again on the name of the same column:
        reverse sort according to the name of this column

## Sorting features:
    1. Column 'Ext':
        folders are sorted by the number of subfolders
    2. Column 'Size':
        folders are sorted by the number of items in the folder

## Keyboard Key Control:
    1. cursor arrows "up" and "down" - move through the list of files
    2. "Escape" - close the menu and the "Help" window
    3. "Ctrl + H" show / hide hidden files

