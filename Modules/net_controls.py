import tkinter as tk
import customtkinter as ctk

from Modules.utils import *
from Modules.custom_button import *



class NetControls(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.kwargs = kwargs
        self.icon_size : tuple = 65, 65
        self.icons : dict[str : tuple] = {
            "Pause" : (load_to_size("pause", *self.icon_size), load_to_size("highlight_pause", *self.icon_size)),
            "Play" : (load_to_size("play", *self.icon_size), load_to_size("highlight_play", *self.icon_size)),
            }

        # Frames =======================================================================

        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", width = 5)
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)

        self.buffer_frame_1.pack(side = "left", fill = "both")
        self.buffer_frame_2.pack(side = "top", fill = "both")

        # Widgets ======================================================================

        self.play_button = CustomButton(self, event = "<<PlayNetwork>>", icons = self.icons["Play"], image = self.icons["Play"][0], background = self.kwargs.get("background"))
        self.pause_button = CustomButton(self, event = "<<PauseNetwork>>", icons = self.icons["Pause"], image = self.icons["Pause"][0], background = self.kwargs.get("background"))
        self.update_speed = ctk.CTkSlider(self, from_ = 0, to = 200)


        self.pause_button.pack(side = "right", padx = (0, 15), pady = 15)
        self.play_button.pack(side = "right", padx = (0, 15), pady = 15)
        self.update_speed.pack(side = "right", padx = 15, pady = 15)