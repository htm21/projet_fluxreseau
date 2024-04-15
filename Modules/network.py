import json
import tkinter as tk

from time import sleep
from time import time
from Modules.net_controls import NetControls
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

    instance_counter = 0

    def __init__(self, parent : tk.Widget, name : str, app : object, *args : tuple, **kwargs : dict) -> None:

        Network.instance_counter += 1
        
        # GUI Stuff ====================================================================
        
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        
        self.app = app
        self.parent = parent
        self.kwargs =  kwargs
        self.icon_size : tuple = 90, 90
        self.icons : dict[str : tuple] = {
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Source" : (load_to_size("source_node", *self.icon_size), load_to_size("highlight_source_node", *self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", *self.icon_size), load_to_size("highlight_buffer_node", *self.icon_size)),
            "Endpoint" : (load_to_size("endpoint_node", *self.icon_size), load_to_size("highlight_endpoint_node", *self.icon_size)),
            "Pause" : (load_to_size("pause", 75, 75), load_to_size("highlight_pause", 75, 75)),
            "Play" : (load_to_size("play", 75, 75), load_to_size("highlight_play", 75, 75)),
            }
        
        self.net_controls = NetControls(self, background = "#22282a")
        self.net_controls.place(anchor = "se", relx = 1, rely = 1)
        self.selected_node = None
        self.bind("<Button-1>", self.select_object)
        self.bind("<B1-Motion>", self.move_node)

        # Logic Stuff ==================================================================
        
        self.name = name
        self.nodes : dict[str or int: Node] = {} # Sources, Endpoints or Buffers in the network
        self.connections : dict = {} # Links between nodes
        self.connection_counter = 0

        self.pause = True
        self.update_speed = 1
        self.last_updated = time()
        self.parametre = poisson_process(2)
        self.arrived_paquets = 0
        self.paquet_loss = 0


    # Logic Functions ====================================================================



    def update_network(self):
        
        print(self.last_updated)
        self.last_updated = time()

        for node in self.connections:
            if self.nodes[node].type == "Source" :
                print(f" SOURCE NAME : {self.nodes[node].name}")
                source = self.nodes[node]
                paq = source.get_paquet()
                if not paq :
                    source.create_paquet("ABCD",2,False)
                    paq = source.get_paquet()
                print(f" LE PAQUET : {paq}")

                for sortie in self.connections[node] :
                    print(f" LA SORTIE EST {sortie} ")

                    if self.nodes[sortie].type == "Buffer" :
                        ex = self.nodes[sortie]
                        print(f" BUFFER -> {ex} ")
                        print(f" LA FILE AVANT RECEPTION : {ex.paquet_queue} ")
                        ex.receve_paquet(source)
                        print(f" LA FILE APRES RECEPTION : {ex.paquet_queue} ")
                    
                    print(" ---------- FIRST TEST DONE ----------")
                    print()
                    

            elif self.nodes[node].type == "Buffer" :
                print(f" BUFFER QUEUE of '{self.nodes[node].name}'  BEFORE SENDING : {self.nodes[node].paquet_queue}")
                paq = self.nodes[node].send_paquet()
                print(f" THE PACKET SENT : {paq}")
                if not paq :
                    continue
                print(f" BUFFER QUEUE AFTER SENDING : {self.nodes[node].paquet_queue}")
                print(" ---------------- SECOND TEST DONE ---------------")
                print()
                

                print(f" THE POSSIBLE CONNECTIONS ARE : {self.connections[node]}")
                for sortie in self.connections[node] :
                    if self.nodes[sortie].type == "Source" :
                        continue
                    if self.nodes[sortie].type == "Endpoint" :
                            print(f"THE DESTINATION HAS BEEN FOUND :    {self.nodes[sortie].type} ---> {self.nodes[sortie].name} ")
                            print("         SENDING INFORMATION     ")
                            self.nodes[sortie].receve_paquet(paq)
                            self.arrived_paquets += 1
                            print(f"   INFORMATION RECEVEIVED, THE PACKET IS NOW AT DESTINATION :  '{self.nodes[sortie]}' ")
                            print(f"  THE NUMBER OF PACKET THAT HAVE REACHED DESTINATION IS ----> {self.arrived_paquets}")
                            print("--------------- THIRD TEST DONE ------------")
                            print()
                    
                    
                    else :
                        if self.nodes[sortie].type == "Buffer":
                            print(f" FOUND A BUFFER : {self.nodes[sortie].name}")
                            print(f" THE CONTENT OF THIS {self.nodes[node].type} IS ACTUALLY  : {self.nodes[node].paquet_queue}")
                            self.nodes[sortie].receve_paquet(self.nodes[node])
                            print(f" THE BUFFER '{self.nodes[sortie].name}'  HAS RECEIVED THE PACKET, THE QUEUE IS NOW : {self.nodes[sortie].paquet_queue}")
                            print(" --------------------- FOURTH TEST DONE -------------------------")
                            print()


    def add_node(self, node_type, name, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network by adding it to the "self.nodes" dictionary which anc be later accessed by the node name or canvas id.
        If no node type is given it defaults to a "Source" type Node
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Node-1  
        '''
        
        if self.nodes.get(name):
            self.app.alert = ("Error", "SameName")
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
        self.app.alert = ("Success", "CreateNode")
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

        self.app.alert = ("Success", "DeletedNode")
        self.event_generate("<<Alert>>")


    def delete_network(self) -> None:
        for node_name in list(self.connections.keys()):
            self.del_node(self.nodes[node_name])
    
        self.app.alert = ("Success", "DeletedNetwork")
        self.event_generate("<<Alert>>")
        self.deselect_object()


    def add_connection(self, node_1 : object, node_2 : object) -> None:
        '''
        Creates a connection between two nodes if it satisfies the linking requirements
        Adds a tuple(node_name, node_name) to the 'self.links' set
        '''

        if node_1.type == "Endpoint":
            node_1, node_2 = node_2, node_1

        if node_1.type == "Buffer" and node_2.type == "Source":
            node_1, node_2 = node_2, node_1

        if node_2.name in self.connections[node_1.name]:
            self.app.alert = ("Error", "ExistingConnection")
            self.event_generate("<<Alert>>")
            return

        elif node_1.type == "Source" and node_2.type == "Source":
            self.app.alert = ("Error", "TwoSources")
            self.event_generate("<<Alert>>")
            return

        elif node_1.type == "Endpoint" and node_2.type == "Endpoint":
            self.app.alert = ("Error","TwoEndpoints")
            self.event_generate("<<Alert>>")
            return

        else:
            self.app.alert = ("Success", "Connection")
            self.event_generate("<<Alert>>")
            self.connection_counter += 1
           
            self.create_line((*self.coords(node_1.id), *self.coords(node_2.id)), width = 10, fill = "#1D2123", activefill = "#22282a", smooth = True, tags = [node_1.name, node_2.name])
            self.tag_raise("node")

            node_1.connections += 1
            self.connections[node_1.name].append(node_2.name)



    # GUI Functions ====================================================================



    def create_paquet(self, node : Node) -> None:
        self.net_controls.place_forget()
        
        if Endpoint.instance_counter > 0:
            if NodeCreationMenu.instance_counter == 0:
                menu = PaquetCreationMenu(self, node = node, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
                menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)
        else:
            self.net_controls.place(anchor = "se", relx = 1, rely = 1)
            self.app.alert = ("Error", "NoEndpoints")
            self.event_generate("<<Alert>>")


    def create_node(self, *args) -> None:
        self.net_controls.place_forget()
        
        if NodeCreationMenu.instance_counter == 0:
            menu = NodeCreationMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
            menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)


    def delete_object(self, *args) -> None:
        if self.selected_node:
            self.del_node(self.selected_node)
        
        else:
            if len(self.connections):
                if DelNetMenu.instance_counter == 0:
                    self.pause = True
                    menu = DelNetMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
                    menu.place(relx = 0.5, rely = 0.5, anchor = "center", width = 600, height = 330) 
            else:
                self.app.alert = ("Error", "EmptyNetwork")
                self.event_generate("<<Alert>>")


    def create_connection(self, *args) -> None:
        self.net_controls.place_forget()

        if len(self.connections) < 2:
            self.net_controls.place(anchor = "se", relx = 1, rely = 1)
            self.app.alert = ("Error", "NotEnoughNodes")
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
            self.net_controls.place(anchor = "se", relx = 1, rely = 1)
            self.app.alert = ("Error", "SelfConnection")
            self.event_generate("<<Alert>>")
            return
        
        self.add_connection(*nodes)
        self.net_controls.place(anchor = "se", relx = 1, rely = 1)


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


    def play_network(self, *args) -> None:
        if not self.nodes: return
        self.pause = False


    def pause_network(self, *args) -> None:
        self.pause = True


    def save_network(self, *args) -> None:
        if not self.nodes:
            self.app.alert = ("Error", "EmptyNetToSave")
            self.event_generate("<<Alert>>")
            return
        
        file_obj = tk.filedialog.asksaveasfile(title = "Where sould we save the save file?", filetypes = [('Json File', '*.json')], defaultextension = [('Json File', '*.json')])
        if not file_obj:
            self.app.alert = ("Error", "NoSavePath")
            self.event_generate("<<Alert>>")
            return
        
        nodes = []
        for node_name in self.connections:
            node_data = {
                "type" : self.nodes[node_name].type,
                "name" : self.nodes[node_name].name,
                "output_speed" : self.nodes[node_name].output_speed,
                "input_speed" : self.nodes[node_name].input_speed,
                "max_send_paquets" : self.nodes[node_name].max_send_paquets,
                "coords" : self.coords(self.nodes[node_name].id)
                }
            
            nodes.append(node_data)

        data = {
            "nodes" : nodes,
            "connections" : self.connections
        }

        with open(file_obj.name, "w") as file:
            json.dump(data, file)
        
        self.app.alert = ("Success", "NetworkSaved")
        self.event_generate("<<Alert>>")


    def load_network(self, *args) -> None:
        file_path = tk.filedialog.askopenfilename(title = "Gimme a save file", filetypes = (('Json File', '*.json'), ("Tous les fichiers", "*.*")))
        if not file_path:
            self.app.alert = ("Error", "NoDataFile")
            self.event_generate("<<Alert>>")
            return

        with open(file_path) as file:
            data = json.load(file)

        self.delete_network()
        
        for node_data in data["nodes"]:
            self.add_node(node_type = node_data["type"], name = node_data["name"], output_speed = node_data["output_speed"], input_speed = node_data["input_speed"], max_send_paquets = node_data["max_send_paquets"],)
            self.moveto(self.nodes[node_data["name"]].id, *node_data["coords"])

        for main_node in data["connections"]:
            for sub_node in data["connections"][main_node]:
                self.add_connection(self.nodes[main_node], self.nodes[sub_node])

        self.app.alert = ("Success", "NetworkLoaded")
        self.event_generate("<<Alert>>")


    def test(self):
        self.add_node("Source", "S1")
        self.add_node("Source", "S2")
        self.add_node("Buffer", "B1")
        # self.add_node("Buffer", "B2")
        self.add_node("Endpoint", "E1")
        self.add_connection(self.nodes["S1"], self.nodes["B1"])
        self.add_connection(self.nodes["S2"], self.nodes["B1"])
        self.add_connection(self.nodes["B1"], self.nodes["E1"])
        # self.add_connection(self.nodes["B2"], self.nodes["E1"])
        # self.add_connection(self.nodes["B2"], self.nodes["B3"])
        # self.add_connection(self.nodes["B3"], self.nodes["E2"])
        # self.add_connection(self.nodes["B3"], self.nodes["E3"])


        self.update_network()
                

# How to click and drag canvas items:
    # https://stackoverflow.com/questions/61834886/how-to-make-a-drag-and-drop-animation-in-tkinter-canvas
                