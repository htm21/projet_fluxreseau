import tkinter as tk
import customtkinter as ctk
 
from Modules.menus import *
from Modules.node import *
from Modules.custom_button import *
from Modules.utils import *



class Tab(tk.Frame):
    
    total_instance_counter = 0
    instance_counter = 0
    
    def __init__(self, parent : tk.Widget, tab_bar : object, name : str, *args : tuple, **kwargs : dict):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        Tab.total_instance_counter += 1
        Tab.instance_counter += 1

        self.tab_bar = tab_bar
        self.kwargs : dict = kwargs
        self.name : str = name
        self.icon_size : tuple = (15, 15)    
        self.icons : dict = {
            "Close" : (load_to_size("close", *self.icon_size), load_to_size("highlight_close", *self.icon_size))
            }
        
        # Widgets ======================================================================
        
        self.tab_name = tk.Label(self, text = self.name, font = f"{font} 12 bold", foreground = "#ffcc22", background = self.kwargs.get("background"))
        self.close = CustomButton(self, parent_obj = self, func_arg = "close", icons = self.icons["Close"], image = self.icons["Close"][0], background = self.kwargs.get("background"))
        self.tab_highlight = tk.Frame(self, height = 5, background = "#ffcc22")

        self.tab_highlight.pack(side = "top", fill = "x")
        self.tab_name.pack(side = "left", anchor = "s", fill = "y")
        self.close.pack(side = "right", anchor = "s", fill = "y", padx = "5")

        self.tab_name.bind("<Button-1>", lambda args : self.tab_bar.switch_tabs(self.name))
        self.tab_highlight.bind("<Button-1>", lambda args : self.tab_bar.switch_tabs(self.name))


    def select(self) -> None:
        self.tab_name.config(foreground = "#ffcc22", background = "#22282a")
        self.tab_highlight.config(background = "#ffcc22")
        self.close.config(background = "#22282a")
        self.config(background = "#22282a")


    def deselect(self) -> None:
        self.tab_name.config(foreground = "#FFFFFF", background = "#171a1c")
        self.tab_highlight.config(background = "#171a1c")
        self.close.config(background = "#171a1c")
        self.config(background = "#171a1c")
    

    def passdown_func(self, arg) -> None:
        if arg == "close":
            self.tab_bar.close_tab(self.name)


class TabBar(tk.Frame):

    def __init__(self, parent, app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)   

        self.app = app
        self.kwargs = kwargs
        self.icon_size : tuple = (25, 25)    
        self.icons : dict = {
            "Add" : (load_to_size("Add", *self.icon_size), load_to_size("highlight_add", *self.icon_size))
            }
        self.tabs : dict[Tab] = dict()
        self.selected_tab : Tab = None

        # Frame & Widgets ==============================================================

        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", height = "5")
        self.add_network_button = CustomButton(self, parent_obj = self, func_arg = "new_tab", icons = self.icons["Add"], image = self.icons["Add"][0], background = self.kwargs.get("background"))

        self.buffer_frame_1.pack(side = "bottom", fill = "x")
        self.add_network_button.pack(side = "right", padx = 5, pady = 5)


    def new_tab(self) -> None:
        if NodeCreationMenu.instance_counter == 1 or DelNetMenu.instance_counter == 1 or PaquetCreationMenu.instance_counter == 1:
            self.app.alert = ("Error", "ExitOfMenu")
            self.event_generate("<<Alert>>")        
            return

        if NewNetworkMenu.instance_counter == 1:
            self.app.alert = ("Error", "OneNetAtATime")
            self.event_generate("<<Alert>>")
            return
        
        temp_tab_name = f"Network-{Tab.total_instance_counter + 1}"
        self.tabs[temp_tab_name] = Tab(parent = self, tab_bar = self, name = temp_tab_name)
        if self.selected_tab: self.selected_tab.deselect()
        self.selected_tab = self.tabs[temp_tab_name]
        self.tabs[temp_tab_name].select()
        self.tabs[temp_tab_name].pack(side = "left", fill = "y")

        self.app.create_network(temp_tab_name)


    def close_tab(self, tab_name) -> None:

        tab_names = list(self.tabs.keys())
        tab_index = tab_names.index(tab_name)

        if right_tab := tab_names[tab_index + 1 : tab_index + 2]:
            self.switch_tabs(right_tab[0])
        elif left_tab := tab_names[tab_index - 1 : tab_index] and left_tab != tab_name:
            self.switch_tabs(left_tab[0])
        else:
            self.selected_tab = None

        self.tabs[tab_name].destroy()
        del self.tabs[tab_name]
        Tab.instance_counter -= 1
        self.app.delete_network(tab_name)

        if len(self.tabs) == 0:
            self.new_tab()


    def switch_tabs(self, tab_name) -> None:
        if self.selected_tab.name == tab_name:
            return 
        
        self.selected_tab.deselect()
        self.tabs[tab_name].select()
        self.app.switch_network(tab_name)
        self.selected_tab = self.tabs[tab_name]


    def passdown_func(self, arg : str) -> None:
        if arg == "new_tab":
            self.new_tab()