import os
import screeninfo
import tkinter as tk
from PIL import Image,ImageTk


app_folder_path = os.getcwd().replace("\\", "/")
font = "Montserrat"
# font = "Arial"


def screen_dimensions(root : tk.Tk) -> tuple[int, int]:
    
    return root.winfo_screenwidth(), root.winfo_screenheight()


def monitor_dimensions() -> tuple[int, int]:
    monitor = screeninfo.get_monitors()[0]
    monitor_width, monitor_height = monitor.width, monitor.height
    
    return monitor_width, monitor_height


# def load_icon(icon : str) -> tk.PhotoImage:
#     return tk.PhotoImage(file = f"{app_folder_path}/Icons/{icon}.png")


def load_to_size(icon : str, width : int, height : int) -> ImageTk.PhotoImage:
    icon = Image.open(f"{app_folder_path}/Icons/{icon}.png")
    icon = icon.resize((width, height), Image.ANTIALIAS)

    return ImageTk.PhotoImage(icon)