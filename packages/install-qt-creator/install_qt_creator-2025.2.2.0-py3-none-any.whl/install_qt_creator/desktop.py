from win32com.client import Dispatch
from pathlib import Path


def create_shortcut1(lnk, dst):
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(lnk))
    shortcut.Targetpath = str(dst)
    shortcut.Arguments = ""
    shortcut.save()


def create_shortcut(dst):
    home_folder = Path.home()
    desktop = home_folder.joinpath(r"Desktop")
    lnk_file = desktop.joinpath("Qt Creator.lnk")

    start_menu = home_folder.joinpath(
        r"AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\StartMenu"
    )
    lnk_file2 = start_menu.joinpath("Qt Creator.lnk")
    create_shortcut1(lnk_file, dst)
    create_shortcut1(lnk_file2, dst)
