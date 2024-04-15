import os
import platform
import screeninfo
import random as rd
import tkinter as tk

from math import log10
from Modules.node import *
from PIL import Image,ImageTk


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
        "CreateNode" :  "Node created!",
        "DeletedNetwork" : "Network deleted!",
        "NetworkLoaded" : "Network loaded!",
        "NetworkSaved" : "Network saved!",
        "CreateNetwork" : "Network created!"
        },
    
    "Error" : {
        "NotEnoughNodes" : "There are not enough nodes to connect!",
        "TwoSources" : "You can't connect two Sources!",
        "TwoEndpoints" : "You can't connect two Endpoints!",
        "ExistingConnection" : "Nodes are already connected!",
        "SameName" : "Two nodes can't have the same name!",
        "SelfConnection" : "You can't connect a node to itself!",
        "EmptyNetwork" : "Network is already empty!",
        "NoEndpoints" : "There are no Endpoint nodes!",
        "NoSavePath" : "No save path given!",
        "NoDataFile" : "No file given!",
        "EmptyNetToSave" : "There is nothing to save!",
        "OneNetAtATime" : "You can only create one network at a time!",
        "ExitOfMenu" : "Exit out of the current menu before creating or switching to a new tab!"
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


def poisson_process(parameter):
    U = rd.uniform(0.1,1)
    sleep = -(1/parameter)*log10(U)
    return sleep

