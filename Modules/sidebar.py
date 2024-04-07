import tkinter as tk

from random import randint
from Modules.utils import *
from Modules.network import Network
from Modules.node import Node, Source, Buffer, Endpoint
from Modules.custom_button import CustomButton



class SideBar(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.icon_size : tuple = 75, 75
        self.icons = {
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Source" : load_to_size("source_node", *self.icon_size),
            "Endpoint" : load_to_size("endpoint_node", *self.icon_size),
            "Buffer" : load_to_size("buffer_node", *self.icon_size),
            "Connection" : (load_to_size("connection", *self.icon_size), load_to_size("highlight_connection", *self.icon_size)), 
            "Info" : (load_to_size("info", *self.icon_size), load_to_size("highlight_info", *self.icon_size)),
            "Network" : load_to_size("network", *self.icon_size),
            "Save" : (load_to_size("save", *self.icon_size), load_to_size("highlighted_save", *self.icon_size)),
            "Load" : (load_to_size("load", *self.icon_size), load_to_size("highlighted_load", *self.icon_size)),
            "Paquet" : (load_to_size("paquet", *self.icon_size), load_to_size("highlighted_paquet", *self.icon_size)),
            "Delete" : (load_to_size("delete", *self.icon_size), load_to_size("highlighted_delete", *self.icon_size))
        }

        # Frames =======================================================================

        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.info = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.object_controls = tk.Frame(self, background = kwargs.get("background"))


        self.controls.pack(side = "top", pady = 15, fill = "x")
        self.buffer_frame_1.pack(side = "top", fill = "x")
        self.info.pack(side = "top", pady = 15, anchor = "n", fill = "both", expand = True)
        self.buffer_frame_2.pack(side = "top", fill = "x")
        self.object_controls.pack(side = "top", pady = 15, fill = "x")

        # Widgets ======================================================================

        self.add_node = CustomButton(self.controls, event = "<<AddNode>>", icons = self.icons["Node"], image = self.icons["Node"][0], text = "    Add Node", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.add_connection = CustomButton(self.controls, event = "<<AddConnection>>", icons = self.icons["Connection"], image = self.icons["Connection"][0], text = "    Add Connection", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_title = tk.Label(self.info, image = self.icons["Network"], text = "    Network Info", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_lable = tk.Label(self.info, justify = "left", anchor = "w", font = f"{font} 15 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.save = CustomButton(self.object_controls, event = "<<SaveNet>>", icons = self.icons["Save"], image = self.icons["Save"][0], background = kwargs.get("background"))
        self.load = CustomButton(self.object_controls, event = "<<LoadNet>>", icons = self.icons["Load"], image = self.icons["Load"][0], background = kwargs.get("background"))
        self.app_info = CustomButton(self.object_controls, event = "<<AppInfo>>", icons = self.icons["Info"], image = self.icons["Info"][0], background = kwargs.get("background"))
        self.add_paquet = CustomButton(self.object_controls, event = "<<CustomPaquet>>", icons = self.icons["Paquet"], image = self.icons["Paquet"][0], background = kwargs.get("background"))
        self.delete = CustomButton(self.object_controls, event = "<<DeleteObject>>", icons = self.icons["Delete"], image = self.icons["Delete"][0], background = kwargs.get("background"))


        self.add_node.pack(side = "top", anchor = "w", padx = 15, pady = (0, 15))
        self.add_connection.pack(side = "top", anchor = "w", padx = 15)
        self.info_title.pack(side = "top", anchor = "w", padx = 15, pady = (0, 15))
        self.info_lable.pack(side = "left", anchor = "nw", padx = (25, 0))
        self.delete.pack(side = "right", padx = 10)
        self.save.pack(side = "right", padx = 10)
        self.load.pack(side = "right", padx = 10)
        self.app_info.pack(side = "right", padx = 10)


    def reset_controls(self):
        self.save.pack_forget()
        self.load.pack_forget()
        self.add_paquet.pack_forget()
        self.app_info.pack_forget()


    def set_object_controls(self, data : object):
        self.reset_controls()

        if data == None: # Network Controls
            self.save.pack(side = "right", padx = 10)
            self.load.pack(side = "right", padx = 10)
            self.app_info.pack(side = "right", padx = 10)

        elif isinstance(data, Node) and data.type != "Endpoint": # Node Controls
            self.add_paquet.pack(side = "right", padx = 10)


    def set_object_info(self, data : object) -> None:

        if isinstance(data, Network): # Network Info
            
            network = data
            self.info_title.config(image = self.icons["Network"], text = f"    {data.name} Info")
            info_text = f"Name : {network.name}\n\nNodes : {len(network.nodes) // 2}\n      Sources : {Source.instance_counter}\n      Endpoints : {Endpoint.instance_counter}\n      Buffers : {Buffer.instance_counter}\n\nConnections : {network.connection_counter}"
            self.info_lable.config(text = info_text)


        elif isinstance(data, Node): # Node Info
            node = data
            self.info_title.config(image = self.icons[node.type], text = f"    {node.name} Info")
            info_text = f"Type : {node.type}\nName : {node.name}\n"
            
            if node.type == "Source":
                info_text += f"\nConnections : {node.connections}"
                info_text += f"\nOutput : {node.output_speed} Units/s"
            
            elif node.type == "Endpoint":
                info_text += f"\nThroughput : {node.input_speed} Units/s"
            
            elif node.type == "Buffer":
                info_text += f"\nConnections : {node.connections}"
                info_text += f"\nOutput : {node.output_speed} Units/s"
                info_text += f"\nThroughput : {node.input_speed} Units/s"

            paquets = "\n    " + "\n    ".join(str(paquet) for paquet in node.paquet_queue[:2])
            if len(node.paquet_queue) > 2:
                paquets += f"\n    And {len(node.paquet_queue) - 2} more..."
            info_text += f"\nPaquet Queue : {paquets}"
            
            self.info_lable.config(text = info_text)
