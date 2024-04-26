import pyglet
import platform
import tkinter as tk

from time import time
from Modules.utils import *
from Modules.menus import *
from Modules.sidebar import *
from Modules.network import *
from Modules.tab_bar import *



class App(object):
    '''
    The "App" class is a central objetc that will manage all GUI elements and logic.
    '''

    # Ajoute la police personnalisée aux familles de polices tkinters afin que la police personnalisée sélectionnée puisse être utilisée
    # La police doit être installée sur le PC de l'utilisateur si on veut l'utiliser
    if platform.system() == "Windows":
        pyglet.font.add_file(f"{app_folder_path}/Font/{font}.ttf") 


    def __init__(self, parent : tk.Tk) -> None:
        
        # tk.Tk() object
        self.parent : tk.Tk = parent
        
        # vars pour gérer la mise à jour et la pause du réseau actuel
        self.Running : bool = True                                    
        self.update_speed : int = 1

        self.icon_size : tuple = 15, 15
        self.icons : dict[str : object]= {
            "Success" : load_to_size("success", *self.icon_size),
            "Error" : load_to_size("error", *self.icon_size)
            }

        # Vars d'alerte utilisés pour gérer le message d'alerte et la durée pendant laquelle il est affiché à l'utilisateur
        self.alert : str = None
        self.alert_on_screen_time : int = 5
        self.alert_create_time : int = 0

        # Vars de réseau utilisés pour gérer et manipuler dans le réseau actuel
        self.network_instances : dict[str : Network] = dict()
        self.current_network : Network = None

        # Window Positioning ===========================================================
        # Centre la fenêtre sur l'écran en fonction de la résolution d'affichage actuelle

        self.screen_w, self.screen_h = screen_dimensions(self.parent)
        self.screen_w_center, self.screen_h_center = self.screen_w // 2, self.screen_h // 2
        
        self.gui_w, self.gui_h = 1280, 720
        self.gui_w_center, self.gui_h_center = self.gui_w // 2, (self.gui_h // 2) + 20
        self.x, self.y = self.screen_w_center - self.gui_w_center, self.screen_h_center - self.gui_h_center

        # Window Settings ==============================================================
        # Configuration des paramètres de la fenêtre tkinter

        self.parent.geometry(f"{self.gui_w}x{self.gui_h}+{self.x}+{self.y}")      
        self.parent.title("Project Transmission")
        self.parent.minsize(1280, 720)
        self.parent.iconbitmap(f"{app_folder_path}/Icons/icon.ico")

        # Frames =======================================================================
        # Initialisation des composants du GUI

        self.Main_Frame = tk.Frame(self.parent, background = "#171a1c", highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.tab_bar = TabBar(self.Main_Frame, app = self, background = "#22282a")
        self.side_bar = SideBar(self.Main_Frame, background = "#22282a", width = 375)
        self.side_bar.pack_propagate(0)

        self.Main_Frame.pack(anchor = "center", fill = "both", expand = True)
        self.tab_bar.pack(side = "top", fill = "x")
        self.tab_bar.new_tab()

        # Widgets ======================================================================

        self.alert_lable = tk.Label(self.parent, compound = "left", font = f"{font} 15 bold", foreground = "#FFFFFF", padx = 10)

        # Binds ========================================================================
        # Les Binds & VirtualEvents sont utilisés dans tout le programme pour exécuter des fonctions entre les composants du GUI
        self.parent.bind("<<Alert>>", self.create_alert)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)



    def create_alert(self, *args : tuple) -> None:
        '''
        Affiche le message d'alerte associé à la clé d'alerte.
        (tous les messages d'alerte et les clés sont stockés dans le fichier Modules.utils.py)
        '''
        text = " " + ALERTS[self.alert[0]][self.alert[1]]
        color = "#4d0000" if self.alert[0] == "Error" else "#004d00"

        self.alert_lable.config(image = self.icons[self.alert[0]], text = text, font = f"{font} 15 bold", foreground = "#FFFFFF", background = color)
        self.alert_create_time = time()
        self.alert_lable.place(anchor = "sw", relx = 0, rely = 1, bordermode = "inside")


    def on_closing(self, *args) -> None:
        '''
        Définit "self.Running" sur "False" lors de la fermeture de la fenêtre via le gestionnaire de fenêtres du Sys.
        '''
        self.Running = False


    def create_network(self, temp_name  : str) -> None:
        '''
        Affiche le menu Création de réseau.
        En fonction de l'état du GUI, les éléments sont d'abord supprimés et mis en pause avant d'être affichés.
        Si l'utilisateur passe à un "Tab" différent avant de terminer la création du réseau, une instance de réseau vide sera ajoutée
        aux "self.network_instances" pour faciliter le passage à un "Tab" vide
        '''

        # Prendre soin de la "Sidebar" avant de l'afficher
        if self.side_bar.winfo_ismapped():
            self.side_bar.pack_forget()

        # Prendre soin du 'Network' actuel avant de l'afficher
        if self.current_network:
            self.current_network.pause = True
            if self.current_network.selected_node: self.current_network.deselect_object()
            self.current_network.pack_forget()
            self.current_network = None

        # Vérifie s'il y a un "Tab" vide (un nom de réseau dans "self.network_instances" sans instance de réseau)
        if temp_name in list(self.network_instances.keys()):
            self.create_network_menu.place(anchor = "center", relwidth = 0.6, relheight = 0.85, relx = 0.5, rely = 0.5)
            return

        # Créez un nom temporaire pour faciliter le passage à un "Tab" vide
        self.network_instances[temp_name] = None

        # Créer l'instance de classe GUI "NewNetworkMenu"
        self.create_network_menu = NewNetworkMenu(self.Main_Frame, app = self, background = "#22282a", highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.create_network_menu.place(anchor = "center", relwidth = 0.6, relheight = 0.85, relx = 0.5, rely = 0.5)


    def delete_network(self, network_name : str) -> None:
        '''
        Supprime une instance « Network » de « self.network_instances » avec le nom du réseau et
        détruit la partie GUI de la classe.
        '''
        if self.network_instances[network_name]: 
            self.network_instances[network_name].destroy()
            Network.instance_counter -= 1
        else:
            NewNetworkMenu.instance_counter -= 1
            self.create_network_menu.place_forget()
        
        del self.network_instances[network_name]



    def add_network(self, name : str, temp_name : str, paquet_size : int):
        '''
        Ajoute une instance « Network » dans self.network_instances avec le nom du réseau comme clé.
        Remplace le nom de réseau temporaire qui a été mis en place pour faciliter le changement d'onglet par un réseau vide
        '''
        
        # Création de l'instance "Network"
        self.network_instances[name] = Network(self.Main_Frame, name = name, paquet_size = paquet_size, app = self, border = 0, highlightthickness = 0, background = "#171a1c")     # initiate a new Network
        
        # Remplacement du nom temporaire du réseau
        self.tab_bar.tabs[name] = self.tab_bar.tabs.pop(temp_name)
        self.tab_bar.tabs[name].name = name
        self.tab_bar.tabs[name].tab_name.config(text = name)

        # Supprimer et placer les objets GUI corrects pour le réseau
        self.create_network_menu.pack_forget()
        self.current_network = self.network_instances[name]
        self.side_bar.pack(side = "right", fill = "y")
        self.current_network.pack(side = "left", fill = "both", expand = True)

        # Mise en place des Binds pour que les événements fassent référence à l'instance "Network" correcte
        self.bind_events()

        # Mise en place des info du Network et une alerte
        self.side_bar.set_object_info(self.current_network)
        self.alert = ("Success", "CreateNetwork")
        self.parent.event_generate("<<Alert>>")


    def switch_network(self, network_name : str) -> None:
        '''
        Gère le changement d'instance "Réseau" lors du changement d'onglet.s.
        '''
        # Met en pause le réseau actuel et arrête de l'afficher
        if self.current_network:
            self.current_network.net_controls.set_play_button()
            self.current_network.pause = True
            self.current_network.deselect_object()
            self.current_network.pack_forget()
        else:
            # si l'utilisateur revient à un onglet vide, il appelle à nouveau le NewNetworkMenu
            self.create_network_menu.instance_counter -= 1
            self.create_network_menu.place_forget()
            self.side_bar.pack(side = "right", fill = "y")
        
        # définit le réseau actuel sur celui vers lequel l'utilisateur bascule
        self.current_network = self.network_instances[network_name]
        if self.current_network:
            self.bind_events()
            self.side_bar.set_object_info(self.current_network)
            self.current_network.pack(side = "left", fill = "both", expand = True)
        else:
            self.create_network(network_name)

    
    def compare_networks(self, *args):
        '''
        Affiche le menu Comparaison de réseau.
        '''

        # mettre le réseau en pause
        self.current_network.pause = True
        
        # Suppression de tous les widgets actuellement affichés
        self.current_network.pack_forget()
        self.side_bar.pack_forget()
        self.tab_bar.pack_forget()

        # crée une instance de la classe "DataAnalysisMenu"
        self.compare_networks_menu = DataAnalysisMenu(self.Main_Frame, app = self, background = "#171a1c")
        self.compare_networks_menu.pack(anchor = "center", fill = "both", expand = True)


    def close_comparison_menu(self) -> None:
        '''
        Ferme le menu Comparaison de réseau.
        '''
        # Supprime le menu d'analyse des données
        self.compare_networks_menu.pack_forget()
        self.compare_networks_menu = None
        
        # remet les widgets du GUI
        self.tab_bar.pack(side = "top", fill = "x")
        self.side_bar.pack(side = "right", fill = "y")
        self.current_network.pack(side = "left", fill = "both", expand = True)


    def bind_events(self) -> None:
        '''
        Lie les "VirtualEvents" personnalisés à l'instance "Network" dans "self.current_network".
        '''
        self.parent.bind("<<AddNode>>", self.current_network.create_node)
        self.parent.bind("<<ObjControls>>", lambda args : self.side_bar.set_object_controls(self.current_network.selected_node))
        self.parent.bind("<<DeleteObject>>", self.current_network.delete_object)
        self.parent.bind("<<DeleteNetwork>>", self.current_network.delete_network)
        self.parent.bind("<<CustomPaquet>>", lambda args : self.current_network.create_paquet(self.current_network.selected_node))
        self.parent.bind("<<AddConnection>>", self.current_network.create_connection)
        self.parent.bind("<<SaveNet>>", self.current_network.save_network)
        self.parent.bind("<<LoadNet>>", lambda args : self.current_network.load_network())
        self.parent.bind("<<Compare>>", self.compare_networks)