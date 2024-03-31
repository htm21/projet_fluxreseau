import os
import platform
import random as rd
import screeninfo
import tkinter as tk

from math import log10
from PIL import Image,ImageTk


app_folder_path = os.getcwd().replace("\\", "/")
font = "Montserrat" if platform.system() == "Windows" else "Arial"


def screen_dimensions(root : tk.Tk) -> tuple[int, int]:
    
    return root.winfo_screenwidth(), root.winfo_screenheight()


def monitor_dimensions() -> tuple[int, int]:
    monitor = screeninfo.get_monitors()[0]
    monitor_width, monitor_height = monitor.width, monitor.height
    
    return monitor_width, monitor_height


def load_to_size(icon : str, width : int, height : int) -> ImageTk.PhotoImage:
    icon = Image.open(f"{app_folder_path}/Icons/{icon}.png")
    icon = icon.resize((width, height), Image.ANTIALIAS)

    return ImageTk.PhotoImage(icon)


def sleep_time(parameter):
    U = rd.uniform(0.1,1)
    sleep = -(1/parameter)*log10(U)
    return sleep