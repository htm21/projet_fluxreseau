import pyglet
import platform
import tkinter as tk

from Modules.sidebar import SideBar
from Modules.network import Network 
from Modules.utils import *



class App:

    if platform.system() == "Windows":
        pyglet.font.add_file(f"{app_folder_path}/Font/{font}.ttf")

    def __init__(self, parent : tk.Tk) -> None:

        self.parent = parent

        monitor_width, monitor_height = monitor_dimensions()
        monitor_width_center, monitor_height_center = monitor_width // 2, monitor_height // 2
        screen_width, screen_height = screen_dimensions(self.parent)

        self.window_width, self.window_height = (screen_width * 65) // 100, (screen_height * 65) // 100
        self.window_width_center, self.window_height_center = self.window_width // 2, self.window_height // 2
        self.x, self.y = monitor_width_center - self.window_width_center, monitor_height_center - self.window_height_center

        self.parent.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")      
        self.parent.title("Project Transmission")
        self.parent.minsize(1280, 720)
        # self.parent.iconbitmap(default = f"{app_folder_path}/Icons/icon.ico") Need to fix later
        self.parent.option_add(font, '19')

        self.Main_Frame = tk.Frame(self.parent)
        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)


        
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 400)
        self.buffer_frame = tk.Frame(self.Main_Frame, background = "#1D2123", width = 5)
        self.network_sandbox = Network(self.Main_Frame, border = 0, highlightthickness = 0, background = "#171a1c")


        self.network_sandbox.pack(side = "left", fill = "both", expand = True)
        self.side_bar.pack(side = "right", fill = "y")
        self.side_bar.pack_propagate(0)
        self.buffer_frame.pack(side = "right", fill = "y")


        self.parent.bind("<<AddNode>>", lambda args : self.network_sandbox.add_node())
        self.parent.bind("<<NodeInfo>>", lambda event: self.side_bar.set_info_data(self.network_sandbox.nodes[self.network_sandbox.find_overlapping(event.x, event.y, event.x, event.y)[-1]])) #  Worst atrocity I've ever done 
        self.parent.bind("<<NetworkInfo>>", lambda args : self.side_bar.set_info_data(self.network_sandbox))

    

    def create_alert(self, type : str, text : str) -> None:
        pass



#  , highlightbackground = "#FFFFFF", highlightthickness = 2









# highlight = "#ffcc22"

# link : #394642

# network
# box : #2E293D
# network_icon : #221F2E

# node
# box : #394642
# icon : #1E2422

# send
# box : #354d33
# arrow : #232a22

# receve
# box : #3d2932
# arrow : #2a2226

# buffer:
# box : #3d3829
# icon : #2a2822