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
    '''
    The "App" class is a central objetc that will manage all GUI elements and logic.
    '''

    # Adds the custom font to tkinters font families so the custom font selected can be used
    # Font must be installed on the users pc if it is to be used
    if platform.system() == "Windows":
        pyglet.font.add_file(f"{app_folder_path}/Font/{font}.ttf") 


    def __init__(self, parent : tk.Tk) -> None:
        
        self.parent : tk.Tk = parent
        self.Running : bool = True                                    
        self.update_speed : int = 1

        self.icon_size : tuple = 15, 15
        self.icons : dict[str : object]= {
            "Success" : load_to_size("success", *self.icon_size),
            "Error" : load_to_size("error", *self.icon_size)
            }

        # Alert vars used to manage the alert message and the amount of time it is displayed to the user
        self.alert : str = None
        self.alert_on_screen_time : int = 5
        self.alert_create_time : int = 0

        # Network vars used to manage and manipulate in the current network 
        self.network_instances : dict[str : object] = dict()
        self.current_network : Network = None

        # Window Positioning ===========================================================
        # Centers the window on screen based on current display resolution

        self.screen_w, self.screen_h = screen_dimensions(self.parent)
        self.screen_w_center, self.screen_h_center = self.screen_w // 2, self.screen_h // 2
        
        self.gui_w, self.gui_h = 1280, 720
        self.gui_w_center, self.gui_h_center = self.gui_w // 2, (self.gui_h // 2) + 20
        self.x, self.y = self.screen_w_center - self.gui_w_center, self.screen_h_center - self.gui_h_center

        # Window Settings ==============================================================
        # Setting up the tkinter window settings

        self.parent.geometry(f"{self.gui_w}x{self.gui_h}+{self.x}+{self.y}")      
        self.parent.title("Project Transmission")
        self.parent.minsize(1280, 720)
        self.parent.iconbitmap(f"{app_folder_path}/Icons/icon.ico")

        # Frames =======================================================================
        # Initializing GUI conponents

        self.Main_Frame = tk.Frame(self.parent, background = "#171a1c", highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.tab_bar = TabBar(self.Main_Frame, app = self, background = "#22282a")
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 375)
        self.side_bar.pack_propagate(0)

        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)
        self.tab_bar.pack(side = "top", fill = "x")
        self.tab_bar.new_tab()

        # Widgets ======================================================================

        self.alert_lable = tk.Label(self.parent, compound = "left", font = f"{font} 15 bold", foreground = "#FFFFFF", padx = 10)

        # Binds ========================================================================
        # Binds & VirtualEvents are used throughout the program to execute functions between GUI conponenets  
        
        self.parent.bind("<<Alert>>", self.create_alert)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)



    def create_alert(self, *args : tuple) -> None:
        '''
        Displays the alert message associated with the alert key.
        (all alert messages and keys are stored in the Modules.utils.py file)
        '''
        text = " " + ALERTS[self.alert[0]][self.alert[1]]
        color = "#4d0000" if self.alert[0] == "Error" else "#004d00"

        self.alert_lable.config(image = self.icons[self.alert[0]], text = text, font = f"{font} 15 bold", foreground = "#FFFFFF", background = color)
        self.alert_create_time = time()
        self.alert_lable.place(anchor = "sw", relx = 0, rely = 1, bordermode = "inside")


    def on_closing(self, *args) -> None:
        '''
        Sets "self.Running" to "False" when closing the window through the window manager.
        '''
        self.Running = False


    def create_network(self, temp_name  : str) -> None:
        '''
        Displays the Network creation menu.
        Depending on the state of the GUI elements are first taken off and paused before displaying.
        If user switches to a diffrent "Tab" before finishing the network creation an empty network instance will be added
        to the "self.network_instances" to facilitate switching to an empty "Tab"
        '''

        # Taking care of the "Sidebar" before displaying
        if self.side_bar.winfo_ismapped():
            self.side_bar.pack_forget()

        # Taking care of the current 'Network' before displaying
        if self.current_network:
            self.current_network.pause = True
            if self.current_network.selected_node: self.current_network.deselect_object()
            self.current_network.pack_forget()
            self.current_network = None

        # Checks if there is an empty "Tab" (a network name in "self.network_instances" without a netowrk instance)
        if temp_name in list(self.network_instances.keys()):
            self.create_network_menu.place(anchor = "center", relwidth = 0.6, relheight = 0.85, relx = 0.5, rely = 0.5)
            return

        # Create a temporary name to facilitate switching to an empty "Tab"
        self.network_instances[temp_name] = None

        # Create the GUI "NewNetworkMenu" class instance
        self.create_network_menu = NewNetworkMenu(self.Main_Frame, app = self, background = "#22282a", highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.create_network_menu.place(anchor = "center", relwidth = 0.6, relheight = 0.85, relx = 0.5, rely = 0.5)


    def delete_network(self, network_name : str) -> None:
        '''
        Removes a "Network" instance from the "self.network_instances" with the network name and
        destroys the GUI part of the of the class.
        '''
        if self.network_instances[network_name]: 
            self.network_instances[network_name].destroy()
            Network.instance_counter -= 1
        else:
            NewNetworkMenu.instance_counter -= 1
            self.create_network_menu.place_forget()
        
        del self.network_instances[network_name]



    def add_network(self, name : str, temp_name : str, paquet_size : int):
        '''
        Adds a "Network" instance in the self.network_instances with the network name as the key.
        Replaces the temporary network name that was put in place to facilitate switching tabs with an empty network
        '''
        
        # Creation of the "Network" instance
        self.network_instances[name] = Network(self.Main_Frame, name = name, paquet_size = paquet_size, app = self, border = 0, highlightthickness = 0, background = "#171a1c")     # initiate a new Network
        
        # Replacing the temporary name of the network
        self.tab_bar.tabs[name] = self.tab_bar.tabs.pop(temp_name)
        self.tab_bar.tabs[name].name = name
        self.tab_bar.tabs[name].tab_name.config(text = name)

        # Removing and placing correct GUI objects for the network
        self.create_network_menu.pack_forget()
        self.current_network = self.network_instances[name]
        self.side_bar.pack(side = "right", fill = "y")
        self.current_network.pack(side = "left", fill = "both", expand = True)

        # Setting Binds so events reference the correct "Network" instance
        self.bind_events()

        # Setting Network info and alert
        self.side_bar.set_object_info(self.current_network)
        self.alert = ("Success", "CreateNetwork")
        self.parent.event_generate("<<Alert>>")


    def switch_network(self, network_name : str) -> None:
        '''
        Manages the switching of "Network" instances when switching tabs.
        '''
        # Pauses current network and stops displaying it
        if self.current_network:
            self.current_network.net_controls.set_play_button()
            self.current_network.pause = True
            self.current_network.deselect_object()
            self.current_network.pack_forget()
        else:
            # if the user is switching back to an empty tab it calls the NewNetworkMenu again
            self.create_network_menu.instance_counter -= 1
            self.create_network_menu.place_forget()
            self.side_bar.pack(side = "right", fill = "y")
        
        # sets the current network to the one the user is switching to
        self.current_network = self.network_instances[network_name]
        if self.current_network:
            self.bind_events()
            self.side_bar.set_object_info(self.current_network)
            self.current_network.pack(side = "left", fill = "both", expand = True)
        else:
            self.create_network(network_name)

    
    def compare_networks(self, *args):
        '''
        Displays the Network comparison menu.
        '''

        # pausing the network
        self.current_network.pause = True
        
        # Removing any widgets that are currently displaying
        self.current_network.pack_forget()
        self.side_bar.pack_forget()
        self.tab_bar.pack_forget()

        # creates an instance of the "DataAnalysisMenu" class
        self.compare_networks_menu = DataAnalysisMenu(self.Main_Frame, app = self, background = "#171a1c")
        self.compare_networks_menu.pack(anchor = "center", fill = "both", expand = True)


    def close_comparison_menu(self) -> None:
        '''
        Closes the Network comparison menu.
        '''
        # removes the DataAnalysisMenu menu
        self.compare_networks_menu.pack_forget()
        self.compare_networks_menu = None
        
        # puts back the GUI widgets  
        self.tab_bar.pack(side = "top", fill = "x")
        self.side_bar.pack(side = "right", fill = "y")
        self.current_network.pack(side = "left", fill = "both", expand = True)


    def bind_events(self) -> None:
        '''
        Binds the custom "VirtualEvents" to the "self.current_network" "Network" instance. 
        '''
        self.parent.bind("<<AddNode>>", self.current_network.create_node)
        self.parent.bind("<<ObjControls>>", lambda args : self.side_bar.set_object_controls(self.current_network.selected_node))
        self.parent.bind("<<DeleteObject>>", self.current_network.delete_object)
        self.parent.bind("<<DeleteNetwork>>", self.current_network.delete_network)
        self.parent.bind("<<CustomPaquet>>", lambda args : self.current_network.create_paquet(self.current_network.selected_node))
        self.parent.bind("<<AddConnection>>", self.current_network.create_connection)
        self.parent.bind("<<SaveNet>>", self.current_network.save_network)
        self.parent.bind("<<LoadNet>>", lambda args : self.current_network.load_network())
        self.parent.bind("<<Compare>>", self.compare_networks)