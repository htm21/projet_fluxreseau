import PIL
import tkinter as tk

from Modules.node import Node, Source, Buffer, Endpoint
from Modules.utils import *



class Network(tk.Canvas):

    def __init__(self, parent, name : str = None, *args,**kwargs) -> None:
        
        # GUI Stuff ====================================================================
        
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        self.icon_size = 90
        self.icons : dict[str : tuple[PIL.ImageTk, PIL.ImageTk]] = {
            "Node" : (load_to_size("node", self.icon_size, self.icon_size), load_to_size("highlight_node", self.icon_size, self.icon_size)),
            "Source" : (load_to_size("source_node", self.icon_size, self.icon_size), load_to_size("highlight_source_node", self.icon_size, self.icon_size)),
            "Endpoint" : (load_to_size("endpoint_node", self.icon_size, self.icon_size), load_to_size("highlight_endpoint_node", self.icon_size, self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", self.icon_size, self.icon_size), load_to_size("highlight_buffer_node", self.icon_size, self.icon_size)),
            } # dictionary that holds the normal node image and also the highlighted node image
        self.canvasid_to_node : dict[int : str] = {} 
        self.selected_node = None
        self.bind('<Button-1>', self.select_node)
        
        # Logic Stuff ==================================================================
        
        self.name = name if name else f"Network"
        self.nodes : dict[str : Node] = {} # Sources, Endpoints or Buffers in the network
        self.links : set[tuple[str, str]] = set() # Links between nodes
        self.NODE_TYPES = {
            "Source" : Source,
            "Endpoint" : Endpoint,
            "Buffer" : Buffer,
            "Node" : Node
            }


    def add_node(self, node_type = "Node", name = None, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network object by adding it to the "self.nodes" dictionary.
        If no node type is given it defaults to a "Node" type Node (Not defined node)
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Node-1  
        '''

        class_type = self.NODE_TYPES.get(node_type)
        
        if not class_type:
            raise KeyError(f" '{node_type}' is not a valid node type")
        
        if not name:
            name = f"{node_type}-{self.NODE_TYPES.get(node_type).instance_counter}"
        

        canvas_node = self.create_image(self.winfo_width() // 2, self.winfo_height() // 2, image = self.icons[node_type][0])
        # Creating canvas object with "node_type" in the middle of the Canvas

        self.canvasid_to_node[canvas_node] = name
        # Use the Canvas object Id to link the Node object with its corresponding Canvas object

        self.nodes[name] = self.NODE_TYPES.get(node_type)(node_id = canvas_node, name = name, node_type = node_type, *args, **kwargs)
        # Use Node name to acces the node object in the dict of nodes


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
            self.links.add((node_1, node_2))

    
    def info(self):
        '''
        Outputs a simple overview of the networks state
        '''
       
        print()
        
        print(f"{self.name}")
        print(f"\nNodes : {len(self.nodes)}")
        print(f"    Sources : {Source.instance_counter}")
        print(f"    Endpoints : {Endpoint.instance_counter}")
        print(f"    Buffers : {Buffer.instance_counter}")
        print(f"\nConnections : {len(self.links)}")
        for connection in self.links:
            print(f"    {connection[0]} | {connection[1]}")
        
        print()


    def get_node_from_canvas_id(self, canvas_id : int) -> Node:
        return self.nodes[self.canvasid_to_node[canvas_id]]


    def select_node(self, event):
        
        node_ids = self.find_overlapping(event.x, event.y, event.x, event.y)
        if not node_ids:
            self.deselect_node()
            return

        if self.selected_node:
            self.deselect_node()
        
        node_id = node_ids[0]
        node = self.get_node_from_canvas_id(node_id)
        self.selected_node = node
        self.itemconfig(node.id, image = self.icons[node.type][1])
    
        self.addtag_withtag("selected", node_id)
        self.bind("<B1-Motion>", self.move_node)
        

    def deselect_node(self, *args):
        self.itemconfig(self.selected_node.id, image = self.icons[self.selected_node.type][0])
        self.dtag("selected")


    def move_node(self, event):
        self.coords("selected", event.x, event.y)
        


# How to click and drag canvas items:
    # https://stackoverflow.com/questions/61834886/how-to-make-a-drag-and-drop-animation-in-tkinter-canvas

