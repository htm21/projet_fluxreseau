import os
import platform
import random as rd
import screeninfo
import tkinter as tk

from math import log10
from PIL import Image,ImageTk
from Modules.node import Node, Source, Buffer, Endpoint


app_folder_path = os.getcwd().replace("\\", "/")
font = "Montserrat" if platform.system() == "Windows" else "Arial"

NODE_TYPES : dict[str : Node]= {
    "Source" : Source,
    "Endpoint" : Endpoint,
    "Buffer" : Buffer,
    "Node" : Node
    }

ALERTS = {

    "Success": {
        "Connection" : "Connection created!",
        "DeletedNode" : "Node deleted!",
        "CreateNode" :  "Node created!"
        },
    
    "Error" : {
        "NotEnoughNodes" : "There are not enough nodes to connect!",
        "TwoSources" : "You can't connect two Sources",
        "TwoEndpoints" : "You can't connect two Endpoints",
        "ExistingConnection" : "Nodes are already connected!",
        "SameName" : "Two nodes can't have the same name!",
        "SelfConnection" : "You can't connect a node to itself"
        }
    }


def screen_dimensions(root : tk.Tk) -> tuple[int, int]:
    
    return root.winfo_screenwidth(), root.winfo_screenheight()


def monitor_dimensions() -> tuple[int, int]:
    monitor = screeninfo.get_monitors()[0]
    monitor_width, monitor_height = monitor.width, monitor.height
    
    return monitor_width, monitor_height


def load_to_size(icon : str, width : int, height : int) -> ImageTk.PhotoImage:
    icon = Image.open(f"{app_folder_path}/Icons/{icon}.png")
    icon = icon.resize((width, height))

    return ImageTk.PhotoImage(icon)


def sleep_time(parameter):
    U = rd.uniform(0.1,1)
    sleep = -(1/parameter)*log10(U)
    return sleep