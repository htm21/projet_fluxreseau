import tkinter as tk

from time import sleep
from time import time
from Modules.node import Node
from Modules.menus import NodeCreationMenu, DelNetMenu, PaquetCreationMenu
from Modules.utils import *
from Modules.paquet import *


def source_to_buffer(paquet) :
    size = paquet.size
    return size / 100

def buffer_to_buffer(paquet) :
    size = paquet.size
    return size / 2.5


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
        self.bind("<Button-1>", self.select_object)
        self.bind("<B1-Motion>", self.move_node)
        
        # Logic Stuff ==================================================================
        
        self.name = name if name else f"Network"
        self.nodes : dict[str or int: Node] = {} # Sources, Endpoints or Buffers in the network
        self.connections : dict = {} # Links between nodes
        self.connection_counter = 0

        self.pause = False
        self.last_updated = time()
        self.parametre = poisson_process(2)
        self.arrived_paquets = 0
        self.paquet_loss = 0



    # Logic Functions ====================================================================



    def update_network(self):
        
        print(self.last_updated)
        self.last_updated = time()
        
        # for node in self.connections:

        #     if self.nodes[node].type == "Source" :
        #         paq = self.nodes[node].send_paquet()
        #         print(f" ACTUAL PAQUET : {paq}")

        #         if not paq :
        #             self.nodes[node].create_paquet("E3", "ABCD",30,False)
        #             print(f" ACTUAL QUEUE OF '{self.nodes[node].name}' : {self.nodes[node].paquet_queue}")         # probleme avec paquets
        #             paq = self.nodes[node].send_paquet()
        #             print(f" NEW PACKET CREATED : {paq}")
        #             print(f" ACTUAL QUEUE OF '{self.nodes[node].name}' AFTER : {self.nodes[node].paquet_queue}")



        #         for exit in self.connections[node] :
        #             print(f"THE EXIT IS : {exit}")
        #             if self.nodes[exit].type == "Buffer":
        #                 print(f" IS BUFFER : {self.nodes[exit]} ")
        #                 e = self.nodes[exit]
        #                 print(f" BUFFER BEFORE : {e.paquet_queue}")
        #                 sleep(source_to_buffer(paq))
        #                 e.receve_paquet(paq)
        #                 print(f" BUFFER AFTER RECEPTION : {e.paquet_queue}")
                        

        #             if self.nodes[exit].type == "Endpoint" :
        #                 sleep(self.parametre)
        #                 self.nodes[exit].receve_paquet(paq)
        #                 self.arrived_paquets += 1
        #             print(" ---------- FIRST TEST DONE ----------")
        #             print()
                    

        #     elif self.nodes[node].type == "Buffer" :
        #         print(f" BUFFER QUEUE of '{self.nodes[node].name}'  BEFORE SENDING : {self.nodes[node].paquet_queue}")
        #         paq = self.nodes[node].send_paquet()
        #         destination_name = paq.endpoint
        #         print(f" THE DESTINATION NAME OF THE PACKET : {destination_name}")
        #         print(f" THE PACKET SENT : {paq}")
        #         if not paq :
        #             continue
        #         print(f" BUFFER QUEUE AFTER SENDING : {self.nodes[node].paquet_queue}")
        #         print(" ---------------- SECOND TEST DONE ---------------")
        #         print()
                

        #         print(f" THE POSSIBLE CONNECTIONS ARE : {self.connections[node]}")
        #         for exit in self.connections[node] :
        #             if self.nodes[exit].type == "Source" :
        #                 continue
        #             if self.nodes[exit].name == destination_name :
        #                     print(f"THE DESTINATION HAS BEEN FOUND :    {self.nodes[exit].type} ---> {self.nodes[exit].name} ")
        #                     print("         SENDING INFORMATION     ")
        #                     sleep(self.parametre)
        #                     self.nodes[exit].receve_paquet(paq)
        #                     self.arrived_paquets += 1
        #                     print(f"   INFORMATION RECEVEIVED, THE PACKET IS NOW AT DESTINATION :  '{self.nodes[exit]}' ")
        #                     print(f"  THE NUMBER OF PACKET THAT HAVE REACHED DESTINATION IS ----> {self.arrived_paquets}")
        #                     print("--------------- THIRD TEST DONE ------------")
        #                     print()
                    
                    
        #             else :
        #                 if self.nodes[exit].type == "Buffer":
        #                     print(f" FOUND A BUFFER : {self.nodes[exit].name}")
        #                     print(f" THE CONTENT OF THIS {self.nodes[node].type} IS ACTUALLY  : {self.nodes[node].paquet_queue}")
        #                     sleep(buffer_to_buffer(paq))
        #                     self.nodes[exit].receve_paquet(paq)
        #                     print(f" THE BUFFER '{self.nodes[exit].name}'  HAS RECEIVED THE PACKET, THE QUEUE IS NOW : {self.nodes[exit].paquet_queue}")
        #                     print(" --------------------- FOURTH TEST DONE -------------------------")
        #                     print()


    def add_node(self, node_type, name, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network by adding it to the "self.nodes" dictionary which anc be later accessed by the node name or canvas id.
        If no node type is given it defaults to a "Source" type Node
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Node-1  
        '''
        
        if self.nodes.get(name):
            self.alert = ("Error", "SameName")
            self.event_generate("<<Alert>>")
            return

        canvas_node = self.create_image(self.winfo_width() // 2, self.winfo_height() // 2, image = self.icons[node_type][0], tags = "node")
        # Creating canvas object with "node_type" in the middle of the Canvas
        
        node = NODE_TYPES.get(node_type)(node_id = canvas_node, name = name, node_type = node_type, *args, **kwargs)
        # Creating the node object with "node_type"

        self.nodes[canvas_node] = node
        self.nodes[name] = node
        self.connections[name] = []
        # Use Node name or canvas_id to acces the node object in the dict of nodes

        self.tag_raise("node")
        self.alert = ("Success", "CreateNode")
        self.event_generate("<<Alert>>")


    def del_node(self, node : Node) -> None:
        '''
        Deletes a Node from the network by deleting the node from the "self.nodes" dictionary 
        and deleting all existing links to the deleted node from the "self.links" set.
        '''
        
        self.deselect_object()
        if not node: return

        NODE_TYPES[node.type].instance_counter -= 1
        self.connection_counter -= len(self.connections[node.name])
        del self.connections[node.name]        
        for main_node in self.connections:
            for sub_node in self.connections[main_node]:
                if sub_node == node.name:
                    self.connections[main_node].remove(node.name)
                    self.nodes[main_node].connections -=1
                    self.connection_counter -= 1


        if canvas_lines := self.find_withtag(node.name):
            for line in canvas_lines:
                self.delete(line)
        
        self.delete(node.id)
        del self.nodes[node.name]
        del self.nodes[node.id]

        self.alert = ("Success", "DeletedNode")
        self.event_generate("<<Alert>>")


    def delete_network(self) -> None:
        for node_name in list(self.connections.keys()):
            self.del_node(self.nodes[node_name])
    
        self.alert = ("Success", "DeletedNetwork")
        self.event_generate("<<Alert>>")
        self.deselect_object()


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
           
            self.create_line((*self.coords(node_1.id), *self.coords(node_2.id)), width = 10, fill = "#1D2123", activefill = "#22282a", smooth = True, tags = [node_1.name, node_2.name])
            self.tag_raise("node")

            node_1.connections += 1
            self.connections[node_1.name].append(node_2.name)



    # GUI Functions ====================================================================



    def create_paquet(self, node : Node) -> None:
        self.pause = True
        if Endpoint.instance_counter > 0:
            if NodeCreationMenu.instance_counter == 0:
                menu = PaquetCreationMenu(self, node = node, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
                menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)
        else:
            self.alert = ("Error", "NoEndpoints")
            self.event_generate("<<Alert>>")
        self.pause = False


    def create_node(self, *args) -> None:
        self.pause = True
        if NodeCreationMenu.instance_counter == 0:
            menu = NodeCreationMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
            menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)
        self.pause = False
    

    def delete_object(self, *args) -> None:
        self.pause = True
        if self.selected_node:
            self.del_node(self.selected_node)
        
        else:
            if len(self.connections):
                if DelNetMenu.instance_counter == 0:
                    menu = DelNetMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
                    menu.place(relx = 0.5, rely = 0.5, anchor = "center", width = 600, height = 330) 
            else:
                self.alert = ("Error", "EmptyNetwork")
                self.event_generate("<<Alert>>")
        self.pause = False

    def create_connection(self, *args) -> None:
        self.pause = True
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

        if nodes[0] == nodes[1]:
            self.alert = ("Error", "SelfConnection")
            self.event_generate("<<Alert>>")
            return
        
        self.add_connection(*nodes)
        self.pause = False


    def select_object(self, event):   
        object_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor      
        if not object_ids: self.deselect_object(); return
        if self.selected_node: self.deselect_object()
        if not "node" in self.gettags(object_ids[-1]): self.deselect_object(); return

        node = self.nodes[object_ids[-1]]
        self.selected_node = node

        self.event_generate("<<ObjControls>>")
        self.itemconfig(node.id, image = self.icons[node.type][1])
        self.addtag_withtag("selected", node.id)
        

    def deselect_object(self):
        if self.selected_node:
            self.itemconfig(self.selected_node.id, image = self.icons[self.selected_node.type][0])
        self.selected_node = None
        self.event_generate("<<ObjControls>>")
        self.dtag("selected")


    def move_node(self, event):
        if not self.selected_node: return
        self.coords("selected", event.x, event.y)
        if canvas_lines := self.find_withtag(self.selected_node.name):
            for line in canvas_lines:
                nodes = self.gettags(line)
                x1, y1 = self.coords(self.nodes[nodes[0]].id)
                x2, y2 = self.coords(self.nodes[nodes[1]].id)
                self.coords(line, x1, y1, x2, y2)
        



    def test(self):
        self.add_node("Source", "S1")
        self.add_node("Source", "S2")
        self.add_node("Buffer", "B1")
        self.add_node("Buffer", "B2")
        self.add_node("Endpoint", "E1")
        self.add_node("Buffer", "B3")
        self.add_node("Endpoint", "E2")
        self.add_node("Endpoint", "E3")
        self.add_connection(self.nodes["S1"], self.nodes["B1"])
        self.add_connection(self.nodes["S2"], self.nodes["B1"])
        self.add_connection(self.nodes["B1"], self.nodes["B2"])
        self.add_connection(self.nodes["B2"], self.nodes["E1"])
        self.add_connection(self.nodes["B2"], self.nodes["B3"])
        self.add_connection(self.nodes["B3"], self.nodes["E2"])
        self.add_connection(self.nodes["B3"], self.nodes["E3"])


        self.update_network()
                

# How to click and drag canvas items:
    # https://stackoverflow.com/questions/61834886/how-to-make-a-drag-and-drop-animation-in-tkinter-canvas
                