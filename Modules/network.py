import json
import tkinter as tk


from time import time
from Modules.menus import *
from Modules.utils import *
from Modules.paquet import *



class Network(tk.Canvas):

    instance_counter = 0

    def __init__(self, parent : tk.Widget, name : str, app : object, paquet_size : int = 10, *args : tuple, **kwargs : dict) -> None:

        Network.instance_counter += 1
        
        # GUI Stuff ====================================================================
        
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        
        self.app = app
        self.parent : tk.Frame = parent
        self.kwargs : dict[str] =  kwargs
        self.icon_size : tuple = 90, 90
        self.icons : dict[str : tuple] = {
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Source" : (load_to_size("source_node", *self.icon_size), load_to_size("highlight_source_node", *self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", *self.icon_size), load_to_size("highlight_buffer_node", *self.icon_size)),
            "Endpoint" : (load_to_size("endpoint_node", *self.icon_size), load_to_size("highlight_endpoint_node", *self.icon_size)),
            "Pause" : (load_to_size("pause", 75, 75), load_to_size("highlight_pause", 75, 75)),
            "Play" : (load_to_size("play", 75, 75), load_to_size("highlight_play", 75, 75)),
            }
        
        self.net_controls : tk.Frame = NetControls(self, network = self, background = "#22282a")
        self.net_controls.place(anchor = "se", relx = 1, rely = 1)
        self.selected_node : Node = None
        self.bind("<Button-1>", self.select_object)
        self.bind("<B1-Motion>", self.move_node)

        # Logic Stuff ==================================================================
        
        self.name = name                                     # Name to distinguish each network  
        self.nodes : dict[str or int : Node] = {}            # Sources, Endpoints or Buffers in the network
        self.connections : dict[str : list] = {}             # Links between nodes
        self.connection_counter : int = 0
        self.paquet_size : int = paquet_size

        self.pause : bool = True                           
        self.last_updated : float = time()

        self.total_paquets_created : int = 0                
        self.total_paquets_transfered : int = 0
        self.total_paquets_lost : int = 0
        self.mean_paquet_wait_time : float = 0


    # Logic Functions ====================================================================


    def update_network(self):
        """ Function that enables inter-code interactions to run """
        
        if not self.connections:            
            self.pause_network()
        
        self.last_updated = time()

        for node_name in self.connections:               
            node = self.nodes[node_name]  
            if node.type == "Source":                          
                node.create_paquets()                               # if the node is a Source, we create_paquets()

                self.total_paquets_created += node.paquet_output 
                if node.behaviour == "Buffered":                   
                    self.total_paquets_lost += node.paquet_loss     


        for node_name in self.connections:
            node = self.nodes[node_name]    

            if node.type == "Buffer" and node.connections:        # if the node is a Buffer and have connections, we can send paquets and also collect some
                node.send_paquets()
                node.collect_paquets()

                self.total_paquets_lost += node.paquet_loss                 # update the numbers
                self.total_paquets_transfered += node.paquet_transfer       # ...

                if self.mean_paquet_wait_time == 0:                         
                    self.mean_paquet_wait_time = node.mean_paquet_wait_time
                else:
                    self.mean_paquet_wait_time = (self.mean_paquet_wait_time + node.mean_paquet_wait_time) / 2

        for node_name in self.connections:
            node = self.nodes[node_name]  
            if node.type == "Source" and node.behaviour == "Normal":        # if the node is a "simple Source" (without buffer)
                if node.paquet_queue:                                       
                    node.paquets_lost += len(node.paquet_queue)
                    self.total_paquets_lost += len(node.paquet_queue)
                    node.paquet_queue.clear()


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
        
        node = NODE_TYPES.get(node_type)(node_id = canvas_node, name = name, node_type = node_type, paquet_size = self.paquet_size, *args, **kwargs)
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

        
        if node.type == "Source":                                               
            self.total_paquets_created -= node.paquets_created
            self.total_paquets_lost -= node.paquets_lost
        
        elif node.type == "Buffer":
            self.total_paquets_lost -= node.paquets_lost
            self.total_paquets_transfered -= node.paquets_transfered


        NODE_TYPES[node.type].instance_counter -= 1
        self.connection_counter -= len(self.connections[node.name])
        del self.connections[node.name]        
        for main_node in self.connections:
            for sub_node in self.connections[main_node]:
                if sub_node == node.name:
                    self.connections[main_node].remove(node.name)
                    # self.nodes[main_node].connections -=1
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

        elif node_1.type == "Buffer" and node_2.type == "Buffer":
            self.app.alert = ("Error","TwoBuffers")
            self.event_generate("<<Alert>>")
            return

        else:
            self.app.alert = ("Success", "Connection")
            self.event_generate("<<Alert>>")
            self.connection_counter += 1
           
            self.create_line((*self.coords(node_1.id), *self.coords(node_2.id)), width = 10, fill = "#1D2123", activefill = "#22282a", smooth = True, tags = [node_1.name, node_2.name])
            self.tag_raise("node")

            # node_1.connections += 1
            self.connections[node_1.name].append(node_2.name)
            node_2.connections.append(node_1)



    # GUI Functions ====================================================================



    def create_paquet(self, node : Node) -> None:
        self.deselect_object()
        self.net_controls.place_forget()

        if NodeCreationMenu.instance_counter == 0:
            menu = PaquetCreationMenu(self, node = node, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
            menu.place(relx = 0.5, rely = 0.5, anchor = "center", relwidth = 0.7, relheight = 0.9)
        else:
            self.net_controls.place(anchor = "se", relx = 1, rely = 1)
            self.app.alert = ("Error", "NoEndpoints")
            self.event_generate("<<Alert>>")


    def create_node(self, *args) -> None:
        self.deselect_object()
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
                    self.net_controls.set_play_button()
                    menu = DelNetMenu(self, network = self, background = "#22282a", highlightbackground = "#1D2123", highlightcolor = "#1D2123", highlightthickness = 5)
                    menu.place(relx = 0.5, rely = 0.5, anchor = "center", width = 600, height = 330) 
            else:
                self.app.alert = ("Error", "EmptyNetwork")
                self.event_generate("<<Alert>>")


    def create_connection(self, *args) -> None:
        self.deselect_object()
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
        if not self.nodes:
            self.net_controls.set_play_button()
            return
        self.pause = False


    def pause_network(self, *args) -> None:
        if self.net_controls.pause_button.winfo_ismapped():
            self.net_controls.set_play_button()
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
        
        node_data = []
        for node_name in self.connections:
            node_vars = vars(self.nodes[node_name])
            node_vars.__delitem__("connections")
            node_vars.__delitem__("paquet_queue")
            if self.nodes[node_name].type == "Buffer":
                node_vars.__delitem__("behaviour_types")
            node_vars.update({"coords" : self.coords(self.nodes[node_name].id)})
            
            node_data.append(node_vars)

        data = {
            "network_name" : self.name,
            "paquet_size" : self.paquet_size, 
            "nodes" : node_data,
            "connections" : self.connections
        }

        with open(file_obj.name, "w") as file:
            json.dump(data, file)
        
        self.app.alert = ("Success", "NetworkSaved")
        self.event_generate("<<Alert>>")


    def load_network(self,*, file_path : str = None) -> None:
        if not file_path:
            file_path = tk.filedialog.askopenfilename(title = "Gimme a save file", filetypes = (('Json File', '*.json'), ("Tous les fichiers", "*.*")))
            if not file_path:
                self.app.alert = ("Error", "NoDataFile")
                self.event_generate("<<Alert>>")
                return

        with open(file_path) as file:
            data = json.load(file)

        if data["network_name"] in self.app.tab_bar.tabs and self.app.tab_bar.selected_tab.name != self.name:
            self.app.alert = ("Error", "LoadNetSameName")
            self.event_generate("<<Alert>>")   
            return

        self.delete_network()
        
        # Recreates Nodes
        for node_data in data["nodes"]:
            if node_data["type"] == "Source":
                if node_data["behaviour"] == "Normal":
                    self.add_node(node_type = node_data["type"], name = node_data["name"], output_speed = node_data["output_speed"], behaviour = node_data["behaviour"])
                elif node_data["behaviour"] == "Buffered":
                    self.add_node(node_type = node_data["type"], name = node_data["name"], output_speed = node_data["output_speed"], behaviour = node_data["behaviour"], capacity = node_data["capacity"])
            
            if node_data["type"] == "Buffer":
                self.add_node(node_type = node_data["type"], name = node_data["name"], output_speed = node_data["output_speed"], behaviour = node_data["behaviour"], capacity = node_data["capacity"])
            
            self.moveto(self.nodes[node_data["name"]].id, *node_data["coords"])

        # Recreates connections
        for main_node in data["connections"]:
            for sub_node in data["connections"][main_node]:
                self.add_connection(self.nodes[main_node], self.nodes[sub_node])

        # set network paquet size
        self.paquet_size = data["paquet_size"]
        
        # Set tab name
        self.app.tab_bar.tabs[data["network_name"]] = self.app.tab_bar.tabs.pop(self.name)
        self.app.tab_bar.tabs[self.name].name = data["network_name"]
        self.app.tab_bar.tabs[self.name].select()


        self.app.alert = ("Success", "NetworkLoaded")
        self.event_generate("<<Alert>>")