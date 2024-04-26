import tkinter as tk
import customtkinter as ctk

from Modules.node import *
from Modules.utils import *
from Modules.network import *
from Modules.custom_button import *



class SideBar(tk.Frame):
    '''
    La « SideBar » est un objet GUI qui utilise les propriétés de l'objet « tk.Frame » pour positionner et afficher 
    des contrôles de l'utilisateur (widgets tkinter) et des informations sur le « réseau » ou le « nœud » pour l'utilisateur.
    '''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Toutes les icônes utilisées sur la « SideBar » sont ajustées à une certaine taille et stockées dans « self.icons » en tant qu'« ImageTk.PhotoImage ».
        # Si l'image d'une interface graphique doit montrer une activité (comme le survol d'un bouton), les images ont une version « mise en évidence ». Les deux icônes sont alors stockées sous forme de tuples.
        self.icon_size : tuple = 65, 65
        self.icons : dict = {
            "Network" : load_to_size("network", *self.icon_size),
            "Source" : load_to_size("source_node", *self.icon_size),
            "Buffer" : load_to_size("buffer_node", *self.icon_size),
            "Endpoint" : load_to_size("endpoint_node", *self.icon_size),
            "Compare" : (load_to_size("compare", *self.icon_size), load_to_size("highlight_compare", *self.icon_size)),
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Save" : (load_to_size("save", *self.icon_size), load_to_size("highlight_save", *self.icon_size)),
            "Load" : (load_to_size("load", *self.icon_size), load_to_size("highlight_load", *self.icon_size)),
            "Paquet" : (load_to_size("paquet", *self.icon_size), load_to_size("highlight_paquet", *self.icon_size)),
            "Delete" : (load_to_size("delete", *self.icon_size), load_to_size("highlight_delete", *self.icon_size)),
            "Connection" : (load_to_size("connection", *self.icon_size), load_to_size("highlight_connection", *self.icon_size))
        }

        # Frames =======================================================================
        # Il s'agit de « sous-Frames » qui permettent de séparer et de personnaliser la disposition des widgets sur la « SideBar »
        # Les « self.buffer_frame » sont utilisés pour montrer une séparation des widgets sur l'interface graphique. 
        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", width = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.info = ctk.CTkScrollableFrame(self, fg_color = kwargs.get("background"), corner_radius = 0)
        self.buffer_frame_3 = tk.Frame(self, background = "#1D2123", height = 5)
        self.object_controls = tk.Frame(self, background = kwargs.get("background"))

        self.buffer_frame_1.pack(side = "left", fill = "y")
        self.controls.pack(side = "top", pady = 15, fill = "x")
        self.buffer_frame_2.pack(side = "top", fill = "x")
        self.info.pack(side = "top", pady = 15, anchor = "n", fill = "both", expand = True)
        self.buffer_frame_3.pack(side = "top", fill = "x")
        self.object_controls.pack(side = "top", pady = 15, fill = "x")

        # Widgets ======================================================================
        # Il s'agit des widgets existants (boutons, étiquettes) qui constituent la « SideBar » (barre latérale)
        self.add_node = CustomButton(self.controls, event = "<<AddNode>>", icons = self.icons["Node"], image = self.icons["Node"][0], text = "    Add Node", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.add_connection = CustomButton(self.controls, event = "<<AddConnection>>", icons = self.icons["Connection"], image = self.icons["Connection"][0], text = "    Add Connection", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_title = tk.Label(self.info, image = self.icons["Network"], text = "    Network Info", compound = "left", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.info_lable = tk.Label(self.info, justify = "left", anchor = "w", font = f"{font} 15 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.save = CustomButton(self.object_controls, event = "<<SaveNet>>", icons = self.icons["Save"], image = self.icons["Save"][0], background = kwargs.get("background"))
        self.load = CustomButton(self.object_controls, event = "<<LoadNet>>", icons = self.icons["Load"], image = self.icons["Load"][0], background = kwargs.get("background"))
        self.compare = CustomButton(self.object_controls, event = "<<Compare>>", icons = self.icons["Compare"], image = self.icons["Compare"][0], background = kwargs.get("background"))
        self.add_paquet = CustomButton(self.object_controls, event = "<<CustomPaquet>>", icons = self.icons["Paquet"], image = self.icons["Paquet"][0], background = kwargs.get("background"))
        self.delete = CustomButton(self.object_controls, event = "<<DeleteObject>>", icons = self.icons["Delete"], image = self.icons["Delete"][0], background = kwargs.get("background"))

        self.add_node.pack(side = "top", anchor = "w", padx = 15, pady = (0, 15))
        self.add_connection.pack(side = "top", anchor = "w", padx = 15)
        self.info_title.pack(side = "top", anchor = "w", padx = 15, pady = (0, 15))
        self.info_lable.pack(side = "left", anchor = "nw", padx = (25, 0))
        self.delete.pack(side = "right", padx = 10)
        self.save.pack(side = "right", padx = 10)
        self.load.pack(side = "right", padx = 10)
        self.compare.pack(side = "right", padx = 10)


    def reset_controls(self) -> None:
        '''
        Supprime tous les contrôles qui ne sont pas appropriés pour un autre « Objet » 
        (self.delete n'est pas supprimé car il est approprié pour tous les « Objets »)
        '''

        self.save.pack_forget()
        self.load.pack_forget()
        self.add_paquet.pack_forget()
        self.compare.pack_forget()


    def set_object_controls(self, data : object) -> None:
        '''
        Définit les contrôles appropriés sur la « SideBar » pour l'objet sélectionné 
        '''
        
        self.reset_controls()
        
        if data == None: # Network Controls
            self.save.pack(side = "right", padx = 10)
            self.load.pack(side = "right", padx = 10)
            self.compare.pack(side = "right", padx = 10)

        elif isinstance(data, Node) and data.type != "Endpoint": # Node Controls
            self.add_paquet.pack(side = "right", padx = 10)


    def set_object_info(self, obj : object) -> None:
        '''
        Définit les informations relatives à l'objet sélectionné et les affiche sur la « SideBar »
        '''
        info_text = ""
        
        if isinstance(obj, Network): # MAJ des informations concernant l'object Network 
            network = obj
            self.info_title.config(image = self.icons["Network"], text = f"    {network.name}")
            
            info_text += f"Name : {network.name}\n"
            info_text += f"Connections : {network.connection_counter}\n\n"
            
            info_text += f"Paquet Size : {network.paquet_size}\n"
            info_text += f"Paquet Wait Time : {network.mean_paquet_wait_time : 0.2f}\n\n"
            
            info_text += f"Data Output : {network.data_output}\n"
            info_text += f"Paquet Output : {network.paquet_output}\n\n" 

            info_text += f"Paquets Created : {network.total_paquets_created}\n"
            info_text += f"Paquets Sent : {network.total_paquets_transfered}\n"
            info_text += f"Paquets Lost : {network.total_paquets_lost}" 
            
            
        elif isinstance(obj, Node): # MAJ des informations concernant l'object Node (et ses class héritantes)
            node = obj
            self.info_title.config(image = self.icons[node.type], text = f"    {node.name}")
            
            info_text += f"Type : {node.type}\n"
            info_text += f"Name : {node.name}\n"
            info_text += f"Behaviour : {node.behaviour}\n\n"


            if node.type == "Source":
                info_text += f"Paquet Gen : {node.paquet_output}/s\n\n"          
                info_text += f"Paquets Created : {node.paquets_created}\n"
                info_text += f"Paquets Lost : {node.paquets_lost}\n\n"

                if node.behaviour == "Buffered":
                    info_text += f"Lambda : {node.lambda_const}\n"
                    info_text += f"Buffer Capacity : {node.capacity}\n"
            
            elif node.type == "Buffer":
                info_text += f"Paquets Sent : {node.paquets_transfered}\n"
                info_text += f"Paquets Lost : {node.paquets_lost}\n\n"

                info_text += f"Lambda : {node.lambda_const}\n"
                info_text += f"Buffer Capacity : {node.capacity}\n"
                info_text += f"Current Size : {node.number_element}\n"


            if node.type == "Source" and node.behaviour == "Buffered" or node.type == "Buffer":
                # Ici, nous ne prenons qu'un maximum de 5 paquets (leurs détails : data, ...) pour les afficher sur la « SideBar », permettant de visualiser leurs arrivées
                # S'il y a plus de 5 paquets présents dans le « Node », un nombre représentant le total des paquets restants est affiché.
                
                paquets = "\n● " + "\n● ".join(str(paquet) for paquet in node.paquet_queue[:5])
                if len(node.paquet_queue) > 5:
                    paquets += f"\n And {len(node.paquet_queue) - 5} more..."
                info_text += f"Paquet Queue : {paquets}"
            

        # MAJ des informations du Label
        self.info_lable.config(text = info_text)
