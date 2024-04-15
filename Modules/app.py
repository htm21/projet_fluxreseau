import pyglet
import platform
import tkinter as tk

from time import time
from Modules.utils import *
from Modules.menus import *
from Modules.sidebar import *
from Modules.network import *
from Modules.tab_bar import *



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
        self.network_instances = dict()

        self.alert = None
        self.alert_on_screen_time = 5
        self.alert_create_time = 0
        self.Running = True
        self.current_network = None

        # Window Positioning ===========================================================

        screen_w, screen_h = screen_dimensions(self.parent)
        screen_w_center, screen_h_center = screen_w // 2, screen_h // 2
        
        self.gui_w, self.gui_h = 1280, 720
        self.gui_w_center, self.gui_h_center = self.gui_w // 2, (self.gui_h // 2) + 20
        self.x, self.y = screen_w_center - self.gui_w_center, screen_h_center - self.gui_h_center

        # Window Settings ==============================================================

        self.parent.geometry(f"{self.gui_w}x{self.gui_h}+{self.x}+{self.y}")      
        self.parent.title("Project Transmission")
        self.parent.minsize(1280, 720)
        # self.parent.iconbitmap(default = f"{app_folder_path}/Icons/icon.ico") Need to fix later

        # Frames =======================================================================

        self.Main_Frame = tk.Frame(self.parent, highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.tab_bar = TabBar(self.Main_Frame, app = self, background = "#171a1c")
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 375)
        self.side_bar.pack_propagate(0)

        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)
        self.tab_bar.pack(side = "top", fill = "x")
        self.tab_bar.new_tab()

        # Widgets ======================================================================

        self.alert_lable = tk.Label(self.parent, compound = "left", font = f"{font} 15 bold", foreground = "#FFFFFF", padx = 10)

        # Binds ========================================================================

        self.parent.bind("<<Alert>>", self.create_alert)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_alert(self, *args) -> None:
        text = " " + ALERTS[self.alert[0]][self.alert[1]]
        color = "#4d0000" if self.alert[0] == "Error" else "#004d00"

        self.alert_lable.config(image = self.icons[self.alert[0]], text = text, font = f"{font} 15 bold", foreground = "#FFFFFF", background = color)
        self.alert_create_time = time()
        self.alert_lable.place(anchor = "sw", relx = 0, rely = 1, bordermode = "inside")


    def on_closing(self, *args) -> None:
        self.Running = False


    def create_network(self, temp_name) -> None:

        if self.side_bar.winfo_ismapped():
            self.side_bar.pack_forget()

        if self.current_network:
            self.current_network.pause = True
            self.current_network.deselect_object()
            self.current_network.pack_forget()
            self.current_network = None

        if temp_name in list(self.network_instances.keys()):
            self.create_network_menu.pack(side = "top", fill = "both", expand = True)
            return

        self.network_instances[temp_name] = None
        self.create_network_menu = NewNetworkMenu(self.Main_Frame, app = self, background = "#22282a")
        self.create_network_menu.pack(side = "top", fill = "both", expand = True)


    def delete_network(self, network_name : str) -> None:
        if self.network_instances[network_name]:
            self.network_instances[network_name].destroy()
            Network.instance_counter -= 1
        else:
            NewNetworkMenu.instance_counter -= 1
            self.create_network_menu.pack_forget()
        
        del self.network_instances[network_name]



    def add_network(self, name : str, temp_name : str):
        self.network_instances[name] = Network(self.Main_Frame, name = name, app = self, border = 0, highlightthickness = 0, background = "#171a1c")
        
        self.tab_bar.tabs[name] = self.tab_bar.tabs.pop(temp_name)
        self.tab_bar.tabs[name].name = name
        self.tab_bar.tabs[name].tab_name.config(text = name)

        self.create_network_menu.pack_forget()
        self.current_network = self.network_instances[name]
        self.side_bar.pack(side = "right", fill = "y")
        self.current_network.pack(side = "left", fill = "both", expand = True)
        

        self.bind_events()
        self.side_bar.set_object_info(self.current_network)
        self.alert = ("Success", "CreateNetwork")
        self.parent.event_generate("<<Alert>>")


    def switch_network(self, network_name : str) -> None:
     
        if self.current_network:
            self.current_network.pause = True
            self.current_network.deselect_object()
            self.current_network.pack_forget()
        else:
            self.create_network_menu.instance_counter -= 1
            self.create_network_menu.pack_forget()
            self.side_bar.pack(side = "right", fill = "y")
        
        
        self.current_network = self.network_instances[network_name]
        if self.current_network:
            self.bind_events()
            self.side_bar.set_object_info(self.current_network)
            self.current_network.pack(side = "left", fill = "both", expand = True)
        else:
            self.create_network(network_name)


    def bind_events(self) -> None:
        self.parent.bind("<<AddNode>>", self.current_network.create_node)
        self.parent.bind("<<ObjControls>>", lambda args : self.side_bar.set_object_controls(self.current_network.selected_node))
        self.parent.bind("<<DeleteObject>>", self.current_network.delete_object)
        self.parent.bind("<<DeleteNetwork>>", self.current_network.delete_network)
        self.parent.bind("<<CustomPaquet>>", lambda args : self.current_network.create_paquet(self.current_network.selected_node))
        self.parent.bind("<<AddConnection>>", self.current_network.create_connection)
        self.parent.bind("<<PlayNetwork>>", self.current_network.play_network)
        self.parent.bind("<<PauseNetwork>>", self.current_network.pause_network)
        self.parent.bind("<<SaveNet>>", self.current_network.save_network)
        self.parent.bind("<<LoadNet>>", self.current_network.load_network)


    def unbind_events(self) -> None:
        self.parent.unbind("<<AddNode>>")
        self.parent.unbind("<<ObjControls>>")
        self.parent.unbind("<<DeleteObject>>")
        self.parent.unbind("<<DeleteNetwork>>")
        self.parent.unbind("<<CustomPaquet>>")
        self.parent.unbind("<<AddConnection>>")
        self.parent.unbind("<<PlayNetwork>>")
        self.parent.unbind("<<PauseNetwork>>")
        self.parent.unbind("<<SaveNet>>")
        self.parent.unbind("<<LoadNet>>")






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