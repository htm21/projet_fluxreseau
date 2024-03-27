import tkinter as tk
from Modules.utils import *
from Modules.node import Node, Source, Buffer, Endpoint
from Modules.custom_button import CustomButton

class SideBar(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.text = ""

        self.icons = {"node" : load_to_size("node", 75, 75), "link" : load_to_size("link", 75, 75), "network" : load_to_size("network", 75, 75)}

        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame = tk.Frame(self, background = "#1D2123", height = 5)
        self.info = tk.Frame(self, background = kwargs.get("background"))

        self.controls.pack(side = "top", pady = (30, 15), fill = "x")
        self.buffer_frame.pack(side = "top", fill = "x")
        self.info.pack(side = "top", pady = (15, 0), anchor = "n", fill = "both", expand = True)


        self.add_node = CustomButton(self.controls, event = "<<AddNode>>", image = self.icons["node"], text = "        Add Node", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.add_link = CustomButton(self.controls, image = self.icons["link"], text = "        Add Link", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_title = tk.Label(self.info, image = self.icons["network"], text = "    Network Info", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_lable = tk.Label(self.info, text = self.text, justify = "left", anchor = "w", font = f"{font} 15 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        

        self.add_node.pack(side = "top", padx = 5, pady = (0, 10))
        self.add_link.pack(side = "top", padx = 5, pady = (10, 0), fill = "x")
        self.info_title.pack(side = "top", padx = 5, pady = 5)
        self.info_lable.pack(side = "left", anchor = "nw",padx = 5, pady = 5)

        