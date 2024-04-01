import PIL
import tkinter as tk

from time import time
from Modules.node_creation_menu import NodeCreationMenu
from Modules.node import Node, Source, Buffer, Endpoint
from Modules.utils import *
from Modules.paquet import *



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
        self.alert = None
        self.bind('<Button-1>', self.select_object)
        
        # Logic Stuff ==================================================================
        
        self.name = name if name else f"Network"
        self.nodes : dict[str or int: Node] = {} # Sources, Endpoints or Buffers in the network
        self.connections : dict = {} # Links between nodes
        self.connection_counter = 0

        self.clock = time()
        self.parametre = sleep_time(2)
        self.arrived_paquets = 0
 


    def update_network(self):
        
        for node in self.connections:
            if self.nodes[node].type == "Source" :
                paq = self.nodes[node].send_paquet()
                if not paq :
                    self.nodes[node].create_paquet(self.connections[node][0], "ABCD",2,False)          # probleme avec paquets
                    paq = self.nodes[node].send_paquet()

                if node in self.connections :
                    if self.nodes[self.connections[node][0]].type == "Buffer":
                        self.nodes[self.connections[node][0]].receve_paquet(paq)

                    if self.nodes[self.connections[node][0]].type == "Endpoint" :
                        self.nodes[self.connections[node][0]].receve_paquet(paq)
                        self.arrived_paquets += 1
                    

            elif self.nodes[node].type == "Buffer" :
                paq = self.nodes[node].send_paquet()
                if not paq :
                    continue
                if node in self.connections :

                    if self.nodes[self.connections[node][0]].type == "Source" :
                        continue
                    self.nodes[self.connections[node][0]].receve_paquet(paq)

                    if self.nodes[self.connections[node][0]].type == "Endpoint" :
                        self.arrived_paquets += 1
            
    
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

        self.alert = ("Success", "CreateNode")
        self.event_generate("<<Alert>>")


    def del_node(self, node : str) -> None:
        '''
        Deletes a Node from the network by deleting the node from the "self.nodes" dictionary 
        and deleting all existing links to the deleted node from the "self.links" set.
        '''
        
        if not node: return

        del self.connections[node.name]
        
        for main_node in self.connections:
    
            for sub_node in self.connections[main_node]:
                if sub_node == node.name:
                    self.connections[main_node].remove(node.name)
                    self.nodes[main_node].connections -=1 
        
        NODE_TYPES[node.type].instance_counter -= 1
        self.connection_counter -= 1

        self.delete(node.id)
        del self.nodes[node.name]
        del self.nodes[node.id]

        self.alert = ("Success", "DeletedNode")
        self.event_generate("<<Alert>>")
        self.deselect_object()


    def create_connection(self) -> None:
        if len(self.connections) < 2:
            self.alert = ("Error", "NotEnoughNodes")
            self.event_generate("<<Alert>>")
            return
        
        self.deselect_object()
        self.config(highlightbackground = "#ffcc22", highlightthickness = 5) 
        nodes = []

        while len(nodes) < 2:
            if self.selected_node:
                nodes.append(self.selected_node)
                self.deselect_object()
            self.parent.update()
        
        self.config(highlightthickness = 0)
        self.add_connection(*nodes)


    def add_connection(self, node_1 : object, node_2 : object) -> None:
        '''
        Creates a connection between two nodes if it satisfies the linking requirements
        Adds a tuple(node_name, node_name) to the 'self.links' set
        '''

        if node_1.type == "Endpoint":
            node_1, node_2 = node_2, node_1

        if node_2.name in self.connections[node_1.name]:
            self.alert = ("Error", "ExistingConnection")
            self.event_generate("<<Alert>>")
            return

        elif node_1.type == "Source" and node_2.type == "Source":
            self.alert = ("Error", "TwoSources")
            self.event_generate("<<Alert>>")
            return

        elif node_1.type == "Endpoint" and node_2.type == "Endpoint":
            self.alert = ("Error","TwoEndpoints")
            self.event_generate("<<Alert>>")
            return

        else:
            self.alert = ("Success", "Connection")
            self.event_generate("<<Alert>>")
            self.connection_counter += 1
            node_1.connections += 1
            self.connections[node_1.name].append(node_2.name)


    def select_object(self, event):
        
        node_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor
        
        if not node_ids:
            self.deselect_object()
            return

        if self.selected_node: self.deselect_object()
        
        node_id = node_ids[-1] # Takes the one most in top
        node = self.nodes[node_id]
        self.selected_node = node

        self.event_generate("<<ObjControls>>")
        self.itemconfig(node.id, image = self.icons[node.type][1])
        self.addtag_withtag("selected", node_id)
        self.bind("<B1-Motion>", self.move_node)
        

    def deselect_object(self, *args):
        if self.selected_node:
            self.itemconfig(self.selected_node.id, image = self.icons[self.selected_node.type][0])
        self.selected_node = None
        self.event_generate("<<ObjControls>>")
        self.dtag("selected")


    def move_node(self, event):
        self.coords("selected", event.x, event.y)
        


# How to click and drag canvas items:
    # https://stackoverflow.com/questions/61834886/how-to-make-a-drag-and-drop-animation-in-tkinter-canvas

