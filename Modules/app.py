import pyglet
import platform
import tkinter as tk

from time import time
from Modules.sidebar import SideBar
from Modules.network import Network 
from Modules.utils import *



class App(object):


    if platform.system() == "Windows":
        pyglet.font.add_file(f"{app_folder_path}/Font/{font}.ttf")


    def __init__(self, parent : tk.Tk) -> None:
        self.parent = parent

        self.icon_size = 15, 15
        self.icons = {
            "Success" : load_to_size("success", *self.icon_size),
            "Error" : load_to_size("error", *self.icon_size)
            }
        self.alert_on_screen_time = 5
        self.alert_create_time = 0

        # Window Positioning ===========================================================

        monitor_width, monitor_height = monitor_dimensions()
        monitor_width_center, monitor_height_center = monitor_width // 2, monitor_height // 2
        screen_width, screen_height = screen_dimensions(self.parent)

        self.window_width, self.window_height = (screen_width * 65) // 100, (screen_height * 65) // 100
        self.window_width_center, self.window_height_center = self.window_width // 2, self.window_height // 2
        self.x, self.y = monitor_width_center - self.window_width_center, monitor_height_center - self.window_height_center

        # Window Settings ==============================================================

        self.parent.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")      
        self.parent.title("Project Transmission")
        self.parent.minsize(1280, 720)
        # self.parent.iconbitmap(default = f"{app_folder_path}/Icons/icon.ico") Need to fix later

        # Frames =======================================================================

        self.Main_Frame = tk.Frame(self.parent, highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 400)
        self.buffer_frame = tk.Frame(self.Main_Frame, background = "#1D2123", width = 5)
        self.network_sandbox = Network(self.Main_Frame, border = 0, highlightthickness = 0, background = "#171a1c")

        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)  
        self.network_sandbox.pack(side = "left", fill = "both", expand = True)
        self.side_bar.pack(side = "right", fill = "y")
        self.side_bar.pack_propagate(0)
        self.buffer_frame.pack(side = "right", fill = "y")

        # Widgets ======================================================================

        self.alert_lable = tk.Label(self.Main_Frame, compound = "left", font = f"{font} 15 bold", foreground = "#FFFFFF", padx = 10)

        # Binds ========================================================================

        self.parent.bind("<<AddNode>>", self.network_sandbox.create_node)
        self.parent.bind("<<ObjControls>>", lambda args : self.side_bar.set_object_controls(self.network_sandbox.selected_node))
        self.parent.bind("<<DeleteObject>>", self.network_sandbox.delete_object)
        self.parent.bind("<<DeleteNetwork>>", self.network_sandbox.delete_network)
        self.parent.bind("<<AddConnection>>", self.network_sandbox.create_connection)
        self.parent.bind("<<Alert>>", lambda args : self.create_alert(self.network_sandbox.alert))


    def create_alert(self, alert : tuple) -> None:
        image_padding = " "
        text = image_padding + ALERTS[alert[0]][alert[1]]
        color = "#4d0000" if alert[0] == "Error" else "#004d00"

        self.alert_lable.config(image = self.icons[alert[0]], text = text, background = color)
        self.alert_create_time = time()
        self.alert_lable.place(anchor = "sw", relx = 0, rely = 1)
        

















# Colors ========================================================================

# highlight : "#ffcc22"
# main color = "#22282a"
# blending color : "#1D2123"
# darker color : "#171a1c"

# Connection : #394642

# success
# box : #004d00
# icon : #003300

# error
# box : #4d0000
# icon : #330000

# special paquet
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