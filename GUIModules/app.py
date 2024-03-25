import pyglet
import tkinter as tk
from Modules.utils import*

from GUIModules.sidebar import SideBar
from GUIModules.sandbox import SandBox 




class App:

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
        self.parent.iconbitmap(default = f"{app_folder_path}/Icons/icon.ico")
        self.parent.option_add(font, '19')

        self.Main_Frame = tk.Frame(self.parent)
        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)


        
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 400)
        self.buffer_frame = tk.Frame(self.Main_Frame, background = "#1D2123", width = 5)
        self.sand_box = SandBox(self.Main_Frame, background = "#171a1c")


        self.sand_box.pack(side = "left", fill = "both", expand = True)
        self.side_bar.pack(side = "right", fill = "y")
        self.side_bar.pack_propagate(0)
        self.buffer_frame.pack(side = "right", fill = "y")




#  , highlightbackground = "#FFFFFF", highlightthickness = 2


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
        



