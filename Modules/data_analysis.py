import tkinter as tk
import matplotlib as mpl
import customtkinter as ctk

from Modules.utils import *
from Modules.custom_button import *



class DataAnalysisMenu(tk.Frame):

    def __init__(self, parent, app, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.app = app
        self.kwargs = kwargs
        
        self.icon_size = 100, 100
        self.icons = {
            "Network" : load_to_size("network", *self.icon_size),
            "Compare" : load_to_size("compare", *self.icon_size),
            "Back" : (load_to_size("back", 75, 75), load_to_size("highlight_back", 75, 75))
            }

        self.data_tags = (
            "Name",
            "Paquet Size",
            "Paquets Created",
            "Paquets Transfered",
            "Paquets Lost",
            "Paquet Wait Time",
            "Nodes"
            )
        
        self.network_data : list = self.get_network_data()

        # Main Frame ==================================================================

        self.main_frame = ctk.CTkScrollableFrame(self, fg_color = "#22282a", orientation = "vertical")
        self.main_frame.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.6, relheight = 1)
        
        # Page Title ==================================================================

        self.title_frame = tk.Frame(self.main_frame, background = "#22282a")
        self.page_title = tk.Label(self.title_frame, image = self.icons["Compare"], compound = "left", text = "  Network Comparison", font = f"{font} 35 bold", foreground = "#FFFFFF", background = "#22282a")
        self.buffer_frame_1 = tk.Frame(self.title_frame, background = "#1D2123", height = "5")

        self.title_frame.pack(side = "top", fill = "x", padx = 20)
        self.page_title.pack(side = "top", anchor = "w", pady = 15)
        self.buffer_frame_1.pack(side = "top", fill = "x")

        # Network Data ================================================================

        self.h_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color = "#22282a", orientation = "horizontal", height = 450)
        self.table_title = tk.Label(self.h_scroll_frame, text = "Network Data", font = f"{font} 25 bold underline", foreground = "#FFFFFF", background = "#22282a")
        self.buffer_frame_2 = tk.Frame(self.h_scroll_frame, background = "#1D2123", height = "5")
        self.table_frame = tk.Frame(self.h_scroll_frame, background = "#22282a")
        self.set_table_widgets()
        self.buffer_frame_3 = tk.Frame(self.h_scroll_frame, background = "#1D2123", height = "5")

        self.h_scroll_frame.pack(side = "top", fill = "x", padx = 20, pady = (25, 0))
        self.table_title.pack(side = "top", anchor = "w", pady = (15, 30))
        self.buffer_frame_2.pack(side = "top", fill = "x", padx = 10)
        self.table_frame.pack(side = "top")
        self.buffer_frame_3.pack(side = "top", fill = "x", padx = 10)

        # Network Graphs ==============================================================

        self.graphs_frame = tk.Frame(self.main_frame, background = "#22282a")
        self.graphs_title = tk.Label(self.graphs_frame, text = "Network Graphs", font = f"{font} 25 bold underline", foreground = "#FFFFFF", background = "#22282a")

        self.graphs_frame.pack(side = "top", fill = "x", padx = 20, pady = (25, 0))
        self.graphs_title.pack(side = "top", anchor = "w", pady = (15, 30))

        # Exit Controls ===============================================================

        self.back_button = CustomButton(self, parent_obj = self, func_arg = "go_back", icons = self.icons["Back"], image = self.icons["Back"][0], background = kwargs.get("background"))
        
        self.back_button.place(anchor = "nw", x = 10, y = 10)



    def get_network_data(self) -> None:
        data = []
        
        for network_name in self.app.network_instances:
            if network := self.app.network_instances[network_name]:
                
                data.append({
                    "Name" : network.name,
                    "Paquet Size" : network.paquet_size,
                    "Paquets Created" : network.total_paquets_created,
                    "Paquets Transfered" : network.total_paquets_transfered,
                    "Paquets Lost" : network.total_paquets_lost,
                    "Paquet Wait Time" : network.mean_paquet_wait_time,
                    "Nodes" : len(network.connections)

                })
        
        return data


    def set_table_widgets(self) -> None:
        
        buffer_offset = 1
        tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "300").grid(column = 0, row = 0, rowspan = len(self.data_tags), sticky = "n", padx = 10)

        for row_index, tag in enumerate(self.data_tags):
            tk.Label(self.table_frame, text = tag, font = f"{font} 15 bold", foreground = "#FFFFFF", background = "#22282a").grid(column = buffer_offset, row = row_index, sticky = "w")

        for colum_index, network_data in enumerate(self.network_data):
            tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "300").grid(column = colum_index + buffer_offset + 1, row = 0, rowspan = len(network_data), sticky = "n", padx = 10)
            buffer_offset += 1 
            for row_index, tag in enumerate(self.data_tags):
                tk.Label(self.table_frame, text = network_data[tag], font = f"{font} 15 bold", foreground = "#FFFFFF", background = "#22282a").grid(column = colum_index + buffer_offset + 1, row = row_index)
        
        tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "300").grid(column = len(self.network_data) + buffer_offset + 1, row = 0, rowspan = len(self.data_tags), sticky = "n", padx = 10)
    

    def passdown_func(self, arg) -> None:
        if arg == "go_back":
            self.app.close_comparison_menu()