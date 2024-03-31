import PIL
import tkinter as tk

from time import time
from Modules.node_creation_menu import NodeCreationMenu
from Modules.node import Node, Source, Buffer, Endpoint
from Modules.utils import *



class Network(tk.Canvas):

    def __init__(self, parent, name : str = None, *args,**kwargs) -> None:
        
        # GUI Stuff ====================================================================
        
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        self.icon_size : tuple = 90, 90
        self.icons : dict[str : tuple] = {
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Source" : (load_to_size("source_node", *self.icon_size), load_to_size("highlight_source_node", *self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", *self.icon_size), load_to_size("highlight_buffer_node", *self.icon_size)),
            "Endpoint" : (load_to_size("endpoint_node", *self.icon_size), load_to_size("highlight_endpoint_node", *self.icon_size)),
            } # dictionary that holds the normal node image and also the highlighted node image
        self.selected_node = None
        self.bind('<Button-1>', self.select_node)
        
        # Logic Stuff ==================================================================
        
        self.name = name if name else f"Network"
        self.nodes : dict[str or int: Node] = {} # Sources, Endpoints or Buffers in the network
        self.connections : dict = {} # Links between nodes
        self.clock = time()
        self.parametre = sleep_time(2)



    def update_network(self):
        
        for node in self.nodes:
            if self.clock - node.last_update_time >= self.parametre:
                if node.type == "Source":
                    if node.send_paquet():
                        paquet = node.send_paquet()
                    else :
                        node.create_paquet()
                        paquet = node.send_paquet()
                    for link in self.connections :
                        if node in link :
                            link[1].receve_paquet(paquet)
                
                elif node.type == "Buffer":
                    paquet = node.send_paquet()
                    for link in self.connections :
                        if node in link :
                            pass

        
    
    def create_node(self) -> None:
        if NodeCreationMenu.instance_counter == 0:
            menu = NodeCreationMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
            menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)
        else:
            return


    def add_node(self, node_type, name, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network by adding it to the "self.nodes" dictionary which anc be later accessed by the node name or canvas id.
        If no node type is given it defaults to a "Source" type Node
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Node-1  
        '''
        

        canvas_node = self.create_image(self.winfo_width() // 2, self.winfo_height() // 2, image = self.icons[node_type][0])
        # Creating canvas object with "node_type" in the middle of the Canvas
        
        node = NODE_TYPES.get(node_type)(node_id = canvas_node, name = name, node_type = node_type, *args, **kwargs)
        # Creating the node object with "node_type"

        self.nodes[canvas_node] = node
        self.nodes[name] = node
        self.connections[name] = []
        # Use Node name or canvas_id to acces the node object in the dict of nodes


    def del_node(self, node : str) -> None:
        '''
        Deletes a Node from the network by deleting the node from the "self.nodes" dictionary 
        and deleting all existing links to the deleted node from the "self.links" set.
        '''

        del self.nodes[node] 
        
        for connection in self.links:
            if node in connection:
                del connection


    def create_link(self, node_1 : str, node_2 : str) -> None:
        '''
        Creates a link between two nodes if it satisfies the linking requirements
        Adds a tuple(node_name, node_name) to the 'self.links' set
        '''
        
        if (node_1, node_2) in self.links:

            raise TypeError(f" The two 'Node' are already linked")
        
        elif self.nodes[node_1].type == "Node" or self.nodes[node_2].type == "Node":
            
            raise TypeError(f" Type 'Node' must be defined before linking")

        elif self.nodes[node_1].type == "Source" and self.nodes[node_2].type == "Source":

            raise TypeError(f" Type 'Source' cannot be link to a 'Source' node")
        
        elif self.nodes[node_1].type == "Endpoint" and self.nodes[node_2].type == "Endpoint":

            raise TypeError(f" Type 'Endpoint' cannot be link to a 'Endpoint' node")

        else:
            self.nodes[node_1].connections += 1
            self.nodes[node_2].connections += 1
            self.connections[node_1].append(node_2)
            self.connections[node_2].append(node_1)

    def select_node(self, event):
        
        node_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor
        
        if not node_ids:
            self.event_generate("<<NetworkInfo>>")
            self.deselect_node()
            return

        if self.selected_node:
            self.deselect_node()
        
        self.event_generate("<<NodeInfo>>", x = event.x, y = event.y)
        node_id = node_ids[-1] # Takes the one most in top
        node = self.nodes[node_id]

        self.selected_node = node
        self.itemconfig(node.id, image = self.icons[node.type][1])
    
        self.addtag_withtag("selected", node_id)
        self.bind("<B1-Motion>", self.move_node)
        

    def deselect_node(self, *args):
        if self.selected_node:
            self.itemconfig(self.selected_node.id, image = self.icons[self.selected_node.type][0])
        self.dtag("selected")


    def move_node(self, event):
        self.coords("selected", event.x, event.y)
        


# How to click and drag canvas items:
    # https://stackoverflow.com/questions/61834886/how-to-make-a-drag-and-drop-animation-in-tkinter-canvas

