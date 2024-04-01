import tkinter as tk
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
            "Link" : load_to_size("link", *self.icon_size), 
            "Network" : load_to_size("network", *self.icon_size)}

        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.info = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.object_controls = tk.Frame(self, background = kwargs.get("background"))


        self.controls.pack(side = "top", pady = 30, fill = "x")
        self.buffer_frame_1.pack(side = "top", fill = "x")
        self.info.pack(side = "top", pady = (30, 0), anchor = "n", fill = "both", expand = True)
        self.buffer_frame_2.pack(side = "top", )
        self.object_controls.pack(side = "top", )

        self.add_node = CustomButton(self.controls, event = "<<AddNode>>", icons = self.icons["Node"], image = self.icons["Node"][0], text = "        Add Node", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.add_connection = CustomButton(self.controls, image = self.icons["Link"], text = "    Add Connection", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_title = tk.Label(self.info, image = self.icons["Network"], text = "    Network Info", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_lable = tk.Label(self.info, justify = "left", anchor = "w", font = f"{font} 15 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        

        self.add_node.pack(side = "top", padx = 5, pady = (0, 15))
        self.add_connection.pack(side = "top", padx = 5, pady = (15, 0), fill = "x")
        self.info_title.pack(side = "top", padx = 5, pady = (0, 15))
        self.info_lable.pack(side = "left", anchor = "nw", padx = (25, 0))

    
    def set_info_data(self, data) -> None:

        if isinstance(data, Network):
            network = data
            self.info_title.config(image = self.icons["Network"], text = f"    {data.name} Info")
            info_text = f"Name : {network.name}\n\nNodes : {len(network.nodes) // 2}\n      Sources : {Source.instance_counter}\n      Endpoints : {Endpoint.instance_counter}\n      Buffers : {Buffer.instance_counter}\n\nConnections : {len(network.connections)}"
            self.info_lable.config(text = info_text)

        elif isinstance(data, Node):
            node = data
            self.info_title.config(image = self.icons[node.type], text = f"    {node.name} Info")
            info_text = f"Type : {node.type}\n\nName : {node.name}\n\nCanvas ID : {node.id}\n\nThroughput : {node.output_speed} bytes/s\n\nConnections : {node.connections}\n\nPaquet Queue :\n\n{node.paquet_queue[:5]}"
            self.info_lable.config(text = info_text)