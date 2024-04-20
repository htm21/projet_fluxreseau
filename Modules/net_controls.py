import tkinter as tk
import customtkinter as ctk

from Modules.utils import *
from Modules.custom_button import *



class NetControls(tk.Frame):

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.network = network
        self.kwargs = kwargs
        self.icon_size : tuple = 65, 65
        self.icons : dict[str : tuple] = {
            "Next" : (load_to_size("next", *self.icon_size), load_to_size("highlight_next", *self.icon_size)),
            "Pause" : (load_to_size("pause", *self.icon_size), load_to_size("highlight_pause", *self.icon_size)),
            "Play" : (load_to_size("play", *self.icon_size), load_to_size("highlight_play", *self.icon_size)),
            }

        # Frames =======================================================================

        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", width = 5)
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)

        self.buffer_frame_1.pack(side = "left", fill = "both")
        self.buffer_frame_2.pack(side = "top", fill = "both")

        # Widgets ======================================================================

        self.play_button = CustomButton(self, parent_obj = self, func_arg = "play", icons = self.icons["Play"], image = self.icons["Play"][0], background = self.kwargs.get("background"))
        self.pause_button = CustomButton(self, parent_obj = self, func_arg = "pause", icons = self.icons["Pause"], image = self.icons["Pause"][0], background = self.kwargs.get("background"))
        self.go_farward = CustomButton(self, parent_obj = self, func_arg = "update", icons = self.icons["Next"], image = self.icons["Next"][0], background = self.kwargs.get("background"))

        self.set_play_button()


    def set_pause_button(self):
        self.play_button.pack_forget()

        self.go_farward.pack(side = "right", padx = 15, pady = 15)
        self.pause_button.pack(side = "right", padx = 15, pady = 15)


    def set_play_button(self):
        self.pause_button.pack_forget()

        self.go_farward.pack(side = "right", padx = 15, pady = 15)
        self.play_button.pack(side = "right", padx = 15, pady = 15)


    def passdown_func(self, arg):
        if arg == "play":
            self.set_pause_button()
            self.network.play_network()
        
        elif arg == "pause":
            self.set_play_button()
            self.network.pause_network()
        
        elif arg == "update":
            self.network.update_network()