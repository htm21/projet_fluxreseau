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
        "ExitOfMenu" : "Exit out of the current menu before creating or switching to a new tab!",
        "TwoBuffers" : "You can't connect two Buffers!",
        "SameNetworkName" : "You can't have two networks with the same name!",
        "LoadNetSameName" : "You can't load a network with an existing name!"
        }
    }


def screen_dimensions(root : tk.Tk) -> tuple[int, int]:
    return root.winfo_screenwidth(), root.winfo_screenheight()


def load_to_size(icon : str, width : int, height : int) -> ImageTk.PhotoImage:
    icon = Image.open(f"{app_folder_path}/Icons/{icon}.png")
    icon = icon.resize((width, height))

    return ImageTk.PhotoImage(icon)













# Colors ========================================================================


# highlight : "#ffcc22"
# main color = "#22282a"
# blending color : "#1D2123"
# darker color : "#171a1c"

# Connection : #394642

# info
# box : #394642
# icon : #1E2422

# success
# box : #004d00
# icon : #003300

# error
# box : #4d0000
# icon : #330000

# paquet
# box : #2E293D
# icon : #221F2E

# save / load
# box : #3D3029
# icon : #2E241F

# delete
# box : #3d2932
# icon : #2a2226

# network
# box : #2E293D
# network_icon : #221F2E

# node
# box : #394642
# icon : #1E2422

# source
# box : #354d33
# arrow : #232a22

# endpoint
# box : #3d2932
# arrow : #2a2226

# buffer:
# box : #3d3829
# icon : #2a2822