import tkinter as tk
from Modules.utils import*


class SandBox(tk.Frame):
    def __init__(self, parent, *args,**kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.icon_size = 90
        self.icons = {"endpoint_node" : load_to_size("endpoint_node", self.icon_size, self.icon_size), "node" : load_to_size("node", self.icon_size, self.icon_size), "source_node" : load_to_size("source_node", self.icon_size, self.icon_size),  "buffer_node" : load_to_size("buffer_node", self.icon_size, self.icon_size)}

        self.sandbox = tk.Canvas(self, border = 0, highlightthickness = 0, background = kwargs.get("background"))
        self.sandbox.pack(anchor = "center", fill = "both", expand = True)

        self.sandbox.create_image(100, 100, image = self.icons["source_node"])
        self.sandbox.create_image(200, 200, image = self.icons["endpoint_node"])
        self.sandbox.create_image(300, 300, image = self.icons["buffer_node"])
        self.sandbox.create_image(400, 400, image = self.icons["node"])


        
        self.sandbox.create_line(100, 800, 450, 800, fill = "#394642", width = 4)
        self.sandbox.create_line(450, 800, 800, 800, fill = "#394642", width = 4)

        self.sandbox.create_image(100, 800, image = self.icons["source_node"])
        self.sandbox.create_image(450, 800, image = self.icons["buffer_node"])
        self.sandbox.create_image(800, 800, image = self.icons["endpoint_node"])
