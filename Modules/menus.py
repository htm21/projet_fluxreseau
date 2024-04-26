import json
import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt

from Modules.node import *
from Modules.utils import *
import matplotlib.ticker as ticker
from Modules.custom_button import * 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class NodeCreationMenu(tk.Frame):   

    instance_counter = 0

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        NodeCreationMenu.instance_counter += 1

        self.network = network
        
        self.icon_size : tuple = 70, 70
        self.icons : dict[str : tuple] = {
            "Source" : (load_to_size("source_node", *self.icon_size), load_to_size("highlight_source_node", *self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", *self.icon_size), load_to_size("highlight_buffer_node", *self.icon_size)),
            "Yes" : (load_to_size("yes", 70, 70), load_to_size("highlight_yes", 70, 70)),
            "No" : (load_to_size("no", 70, 70), load_to_size("highlight_no", 70, 70)),
            }

        # Frames =======================================================================

        self.node_choice = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.node_settings = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.type_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.name_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.output_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.input_speed_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.source_behaviour_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.buffer_behaviour_frame = tk.Frame(self.node_settings, background = kwargs.get("background")) 
        self.capacity_frame = tk.Frame(self.node_settings, background = kwargs.get("background")) 
        self.lambda_frame = tk.Frame(self.node_settings, background = kwargs.get("background")) 

        self.node_choice.pack(side = "top", fill = "x", padx = 20, pady = 15)
        self.buffer_frame1.pack(side = "top", fill = "x")
        self.node_settings.pack(side = "top", fill = "both", expand = True, padx = 20, pady = 15)
        self.buffer_frame2.pack(side = "top", fill = "x")
        self.controls.pack(side = "top", fill = "x", padx = 20, pady = 15)
        
        
        # Widgets ======================================================================

        self.choose_node_lable = tk.Label(self.node_settings, text = "Choose A Node", font = f"{font} 40 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.source_choice = CustomButton(self.node_choice, parent_obj = self, func_arg = "Source", image = self.icons["Source"][0], icons = self.icons["Source"], text = "Source Node", compound = "top", font = f"{font} 18 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.buffer_choice = CustomButton(self.node_choice, parent_obj = self, func_arg = "Buffer", image = self.icons["Buffer"][0], icons = self.icons["Buffer"], text = "Buffer Node", compound = "top", font = f"{font} 18 bold", foreground = "#FFFFFF", background = kwargs.get("background")) 
        
        self.node_type_lable = tk.Label(self.type_frame, text = "Type : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.node_class_label = tk.Label(self.type_frame, font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.name_label = tk.Label(self.name_frame, text = "Name : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.name_entry = tk.Entry(self.name_frame, font = f"{font} 17 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.output_label = tk.Label(self.output_frame, text = "Output : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.output_entry = tk.Entry(self.output_frame, font = f"{font} 17 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)

        self.source_behaviour_label = tk.Label(self.source_behaviour_frame, text = "Behaviour : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.source_behaviour_dropdown = ctk.CTkComboBox(self.source_behaviour_frame, state = "readonly", width = 323, height = 40, corner_radius = 0, border_width = 0, font = (f"{font} bold", 20), dropdown_font = (f"{font} bold", 15), text_color = "#FFFFFF", fg_color = "#171a1c", border_color = "#171a1c", button_hover_color = "#ffcc22", values = Source.behaviour_types, command = self.show_source_capacity)

        self.buffer_behaviour_label = tk.Label(self.buffer_behaviour_frame, text = "Behaviour : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.buffer_behaviour_dropdown = ctk.CTkComboBox(self.buffer_behaviour_frame, state = "readonly", width = 323, height = 40, corner_radius = 0, border_width = 0, font = (f"{font} bold", 20), dropdown_font = (f"{font} bold", 15), text_color = "#FFFFFF", fg_color = "#171a1c", border_color = "#171a1c", button_hover_color = "#ffcc22", values = Buffer.behaviour_types)

        self.capacity_label = tk.Label(self.capacity_frame, text = "Capacity : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.capacity_entry = tk.Entry(self.capacity_frame, font = f"{font} 17 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)

        self.lambda_label = tk.Label(self.lambda_frame, text = "Lambda : ", font = f"{font} 23 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.lambda_entry = tk.Entry(self.lambda_frame, font = f"{font} 17 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.create_button = CustomButton(self.controls, parent_obj = self, func_arg = "create", icons = self.icons["Yes"], image = self.icons["Yes"][0], compound = "right", text = "Create  ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.cancel_button = CustomButton(self.controls, parent_obj = self, func_arg = "cancel", icons = self.icons["No"], image = self.icons["No"][0], compound = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))



        self.choose_node_lable.pack(anchor = "center", fill = "x", expand = True)
        
        self.source_choice.pack(side = "left", fill = "x", expand = True)
        self.buffer_choice.pack(side = "left", fill = "x", expand = True)
        
        self.node_type_lable.pack(side = "left")
        self.node_class_label.pack(side = "right")

        self.name_label.pack(side = "left")
        self.name_entry.pack(side = "right")
        
        self.output_label.pack(side = "left")
        self.output_entry.pack(side = "right")

        self.source_behaviour_label.pack(side = "left")
        self.source_behaviour_dropdown.pack(side = "right")
        
        self.buffer_behaviour_label.pack(side = "left")
        self.buffer_behaviour_dropdown.pack(side = "right")

        self.capacity_label.pack(side = "left")
        self.capacity_entry.pack(side = "right")

        self.lambda_label.pack(side = "left")
        self.lambda_entry.pack(side = "right")

        self.create_button.pack(side = "right", padx = (30, 0))
        self.cancel_button.pack(side = "left", padx = (0, 30))


    def create_node(self, *args):
        """ Création d'un Node en fonction des choix de l'utilisateur """
        
        node_type = self.node_class_label.cget("text")              # on recupère le text du choix cliqué par l'utilisateur
        if not node_type: return        
        
        name = self.name_entry.get()

        if node_type == "Source":
            output = int(self.output_entry.get()) if int(self.output_entry.get()) >= 0 else 100
            behaviour = self.source_behaviour_dropdown.get()  

            if behaviour ==  "Normal":
                self.network.add_node(node_type = node_type, name = name, output = output, behaviour = behaviour)
            
            elif behaviour ==  "Buffered":
                capacity = int(self.capacity_entry.get()) if int(self.capacity_entry.get()) >= 0 else 10
                lambda_const = int(self.lambda_entry.get()) if int(self.lambda_entry.get()) >= 0 else 2
                self.network.add_node(node_type = node_type, name = name, output = output, behaviour = behaviour, capacity = capacity, lambda_const = lambda_const)

        elif node_type == "Buffer":
            behaviour = self.buffer_behaviour_dropdown.get()
            capacity = int(self.capacity_entry.get()) if int(self.capacity_entry.get()) >= 0 else 0
            lambda_const = int(self.lambda_entry.get()) if int(self.lambda_entry.get()) >= 0 else 2
            self.network.add_node(node_type = node_type, name = name, behaviour = behaviour, capacity = capacity, lambda_const = lambda_const)

        self.network.net_controls.place(anchor = "se", relx = 1, rely = 1)
        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def cancel_node(self, *args):
        """ Fonction pour annuler la création d'un Node """
        self.network.net_controls.place(anchor = "se", relx = 1, rely = 1)
        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def reset_settings(self) -> None:
        """ Fonction permettant de remttre à 0 les paramètres du Node """
        
        # Frames ======================================
        self.type_frame.pack_forget()
        self.choose_node_lable.pack_forget()
        self.name_frame.pack_forget()
        self.output_frame.pack_forget()
        self.input_speed_frame.pack_forget()
        self.source_behaviour_frame.pack_forget()
        self.buffer_behaviour_frame.pack_forget()
        self.capacity_frame.pack_forget()
        self.lambda_frame.pack_forget()
        
        # Widgets ======================================
        self.output_entry.delete(0, "end")
        self.source_behaviour_dropdown.set(Source.behaviour_types[0])
        self.buffer_behaviour_dropdown.set(Buffer.behaviour_types[0])
        self.capacity_entry.delete(0, "end")
        self.lambda_entry.delete(0, "end")


    def show_source_capacity(self, *args):
        if self.source_behaviour_dropdown.get() == "Buffered":
            self.capacity_entry.delete(0, "end")
            self.capacity_entry.insert(0, "10")
            self.capacity_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            
            self.lambda_entry.delete(0, "end")
            self.lambda_entry.insert(0, "2")
            self.lambda_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            
        elif self.source_behaviour_dropdown.get() == "Normal":
            self.capacity_frame.pack_forget()
            self.lambda_frame.pack_forget()


    def passdown_func(self, arg):
    
        
        if arg == "Source":
            self.reset_settings()
            self.type_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.name_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.node_class_label.config(text = arg, foreground = "#354d33")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{NODE_TYPES[arg].instance_counter + 1}")
            self.output_entry.insert(0, "100")
            
            self.output_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.source_behaviour_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)

            self.node_settings.pack(side = "top", fill = "x", padx = 20, pady = 15)
        
        elif arg == "Buffer":
            self.reset_settings()
            self.type_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.name_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.node_class_label.config(text = arg, foreground = "#3d3829")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{NODE_TYPES[arg].instance_counter + 1}")
            self.capacity_entry.insert(0, "10")
            self.lambda_entry.insert(0, "2")

            self.buffer_behaviour_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.capacity_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)
            self.lambda_frame.pack(padx = 20, pady = 5, fill = "x", expand = True)

            self.node_settings.pack(side = "top", fill = "x", padx = 20, pady = 15)

        elif arg == "create":
            self.create_node()
        
        elif arg == "cancel":
            self.cancel_node()


















class DelNetMenu(tk.Frame):

    instance_counter = 0

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        DelNetMenu.instance_counter += 1

        self.warning_text = "Your are about to delete all of the networks nodes and connections."
        self.confirmation_text = "Are you sure you want to continue?"
        self.network = network
        self.icon_size : tuple = 75, 75
        self.icons : dict[str : tuple] = {
            "Back" : (load_to_size("back", *self.icon_size), load_to_size("highlight_back", *self.icon_size)),
            "Delete" : (load_to_size("delete", *self.icon_size), load_to_size("highlight_delete", *self.icon_size))

            }

        # Frames =======================================================================

        self.info_frame = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame = tk.Frame(self, background = "#1D2123", height = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))
        
        self.info_frame.pack(side = "top", fill = "both", expand = True)  
        self.buffer_frame.pack(side = "top", fill = "x") 
        self.controls.pack(side = "top", fill = "x", pady = 20)

        # Widgets ======================================================================

        self.info_label = tk.Label(self.info_frame, text = self.warning_text, justify = "center", font = f"{font} 20 bold", foreground = "#FFFFFF", background = kwargs.get("background"), wraplength = "575")
        self.confirmation_label = tk.Label(self.info_frame, text = self.confirmation_text, justify = "center", font = f"{font} 20 bold", foreground = "#ffcc22", background = kwargs.get("background"), wraplength = "575")
        self.back_button = CustomButton(self.controls, parent_obj = self, func_arg = "back", icons = self.icons["Back"], image = self.icons["Back"][0], compound = "left", text = "  Back", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.delete_button = CustomButton(self.controls, parent_obj = self, func_arg = "delete", icons = self.icons["Delete"], image = self.icons["Delete"][0], compound = "right", text = "Delete  ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))


        self.info_label.pack(side = "top", pady = (20, 0))
        self.confirmation_label.pack(side = "top", pady = 20)
        self.back_button.pack(side = "left", padx = 20)
        self.delete_button.pack(side = "right", padx = 20)

    def delete_network(self, *args) -> None:
        DelNetMenu.instance_counter -= 1

        self.network.delete_network()
        self.destroy()


    def cancel_deletion(self, *args) -> None:
        DelNetMenu.instance_counter -= 1
        self.destroy()

    def passdown_func(self, arg) -> None:

        if arg == "back":
            self.cancel_deletion()
        
        elif arg == "delete":
            self.delete_network()




















class PaquetCreationMenu(tk.Frame):
    
    instance_counter = 0

    def __init__(self, parent, node : Node, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        PaquetCreationMenu.instance_counter += 1

        self.node = node
        self.network = network

        # Icons ========================================================================

        self.icon_size = 75, 75
        self.icons = {
            "Paquet" : load_to_size("paquet", *self.icon_size),
            "Yes" : (load_to_size("yes", *self.icon_size), load_to_size("highlight_yes", *self.icon_size)),
            "No" : (load_to_size("no", *self.icon_size), load_to_size("highlight_no", *self.icon_size))
            }

        # Page Title ===================================================================

        self.window_title_frame = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.window_title = tk.Label(self.window_title_frame, image = self.icons["Paquet"], compound = "left", justify = "right", text = "  Paquet Creation", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        
        self.window_title_frame.pack(side = "top", fill = "x", padx = 20, pady = 20)
        self.buffer_frame1.pack(side = "top", fill = "x")
        self.window_title.pack(side = "left")
        
        # Paquet Settings ==============================================================

        self.paquet_settings = tk.Frame(self, background = kwargs.get("background"))
        self.data_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 
        self.size_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 
        self.data_lable = tk.Label(self.data_frame, text = "Data : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.data_entry = tk.Entry(self.data_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        self.data_entry.insert(0, f"Hello from {self.node.name}")
        self.size_lable = tk.Label(self.size_frame, text = "Data Size : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.size_entry = tk.Entry(self.size_frame, font = f"{font} 18 bold", borderwidth = 0, selectborderwidth = 0, disabledbackground = "#171a1c", disabledforeground = "#FFFFFF")
        self.size_entry.insert(0, str(self.network.paquet_size))
        self.size_entry.config(state = "disabled")


        self.paquet_settings.pack(side = "top", fill = "x", expand = True, padx = 20, pady = 20)
        self.data_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        self.size_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        self.data_lable.pack(side = "left")
        self.data_entry.pack(side = "right")
        self.size_lable.pack(side = "left")
        self.size_entry.pack(side = "right")

        # Controls =====================================================================

        self.buffer_frame2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))
        self.create_button = CustomButton(self.controls, parent_obj = self, func_arg = "create", icons = self.icons["Yes"], image = self.icons["Yes"][0], compound = "right", text = "Create  ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.cancle_button = CustomButton(self.controls, parent_obj = self, func_arg = "cancel", icons = self.icons["No"], image = self.icons["No"][0], compound = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.buffer_frame2.pack(side = "top", fill = "x")
        self.controls.pack(side = "top", fill = "x")
        self.create_button.pack(side = "right", padx = 15, pady = 15)
        self.cancle_button.pack(side = "left", padx = 15, pady = 15)



    def create_paquet(self, *args) -> None:
        data = self.data_entry.get()
        size = float(self.size_entry.get()) if float(self.size_entry.get()) >= 0 else 0
        self.node.create_paquet(data = data, size = size)
        
        self.network.net_controls.place(anchor = "se", relx = 1, rely = 1)
        PaquetCreationMenu.instance_counter -= 1
        self.destroy()


    def cancel_paquet(self, *args) -> None:
        self.network.net_controls.place(anchor = "se", relx = 1, rely = 1)
        PaquetCreationMenu.instance_counter -= 1
        self.destroy()

    def passdown_func(self, arg) -> None:
        
        if arg == "cancel":
            self.cancel_paquet()
        
        elif arg == "create":
            self.create_paquet()













class NewNetworkMenu(tk.Frame):
    
    instance_counter = 0
    
    def __init__(self, parent, app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        NewNetworkMenu.instance_counter += 1

        self.app = app
        self.kwargs = kwargs
        
        # Icons ========================================================================

        self.icon_size : tuple = (85, 85)  
        self.icons : dict = {
            "Success" : load_to_size("success", 35, 35),
            "NetworkTitle" : load_to_size("network", 100, 100),
            "Yes" : (load_to_size("yes", 75, 75), load_to_size("highlight_yes", 75, 75)),
            "Back" : (load_to_size("back", 75, 75), load_to_size("highlight_back", 75, 75)),
            "NetworkButton" : (load_to_size("network", *self.icon_size), load_to_size("highlight_network", *self.icon_size)),
            "Load" : (load_to_size("load", *self.icon_size), load_to_size("highlight_load", *self.icon_size)),
            }

        # Page Title ===================================================================
        
        self.title_frame = tk.Frame(self, background = self.kwargs.get("background"))
        self.page_title = tk.Label(self.title_frame, image = self.icons["NetworkTitle"], compound = "left", text = "  New Network", font = f"{font} 35 bold", foreground = "#FFFFFF", background = self.kwargs.get("background"))
        self.buffer_frame_2 = tk.Frame(self.title_frame, background = "#1D2123", height = "5")
        
        self.title_frame.pack(side = "top", fill = "x")
        self.page_title.pack(side = "top", anchor = "w", pady = 30, padx = 15)
        self.buffer_frame_2.pack(side = "top", fill = "x", padx = 15)
        
        # Options ======================================================================

        self.option_frame = tk.Frame(self, background = self.kwargs.get("background"))
        self.create_network_button = CustomButton(self.option_frame, parent_obj = self, func_arg = "new", icons = self.icons["NetworkButton"], image = self.icons["NetworkButton"][0], compound = "top", text = "Create\nNetwork", justify = "center", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.load_network_button = CustomButton(self.option_frame, parent_obj = self, func_arg = "load", icons = self.icons["Load"], image = self.icons["Load"][0], compound = "top", text = "Load\nNetwork", justify = "center", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))     


        self.option_frame.pack(anchor = "center", expand = True, fill = "both")
        self.create_network_button.pack(side = "left", anchor = "center", expand = True, padx = (15, 0))
        self.load_network_button.pack(side = "right", anchor = "center", expand = True, padx = (0, 15))
        
        # Settings =====================================================================

        self.settings_frame = tk.Frame(self, background = self.kwargs.get("background"))
        self.name_frame = tk.Frame(self.settings_frame, background = self.kwargs.get("background"))
        self.paquet_size_frame = tk.Frame(self.settings_frame, background = self.kwargs.get("background"))
        self.name_label = tk.Label(self.name_frame, text = "Name :  ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.name_entry = tk.Entry(self.name_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)    
        self.paquet_size_label = tk.Label(self.paquet_size_frame, text = "Paquet Size :  ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.paquet_size_entry = tk.Entry(self.paquet_size_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        self.name_frame.pack(side = "top", anchor = "w", expand = True, fill = "y", padx = 15, pady = 15)
        self.paquet_size_frame.pack(side = "top", anchor = "w", expand = True, fill = "y", padx = 15, pady = 15)
        
        self.name_label.pack(side = "left", anchor = "s")
        self.name_entry.pack(side = "right", anchor = "s")
        self.paquet_size_label.pack(side = "left", anchor = "n")
        self.paquet_size_entry.pack(side = "right", anchor = "n")

        # Controls =====================================================================

        self.control_frame = tk.Frame(self.settings_frame, background = self.kwargs.get("background"))
        self.buffer_frame_3 = tk.Frame(self.control_frame, background = "#1D2123", height = "5")
        self.back_button = CustomButton(self.control_frame, parent_obj = self, func_arg = "go_back", icons = self.icons["Back"], image = self.icons["Back"][0], compound = "left", text = "  Back", font = f"{font} 30 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.create_button = CustomButton(self.control_frame, parent_obj = self, func_arg = "create", icons = self.icons["Yes"], image = self.icons["Yes"][0], compound = "right", text = "Create  ", font = f"{font} 30 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.control_frame.pack(side = "bottom", fill = "x")
        self.buffer_frame_3.pack(side = "top", fill = "x", anchor = "center", padx = 15)
        self.create_button.pack(side = "right", padx = 15, pady = 15)
        self.back_button.pack(side = "left", padx = 15, pady = 15)


    def create_network(self, name : str = None, paquet_size : int = None) -> None:
        if name == None:
            name = self.name_entry.get()
            paquet_size = int(self.paquet_size_entry.get()) if int(self.paquet_size_entry.get()) >= 0 else 10

            if name in self.app.network_instances and self.app.network_instances[name]:
                self.app.alert = ("Error", "SameNetworkName")
                self.event_generate("<<Alert>>")
                return

            self.app.add_network(name = name, temp_name = self.app.tab_bar.selected_tab.name, paquet_size = paquet_size)
     
        else:
            self.app.add_network(name = name, temp_name = self.app.tab_bar.selected_tab.name, paquet_size = paquet_size)
        
        NewNetworkMenu.instance_counter -= 1
        self.destroy()


    def passdown_func(self, arg : str):
        '''
        Handles all commands from the "CustomButton" widgets
        In this menu there are 4 commands:
            - new : goes to the create network menu
            - load : calls the "tk.filedialog.askopenfilename" function so the user can select a save file to load
            - go_back : goes back to the options menu (load or create network)
            - create : calls the "self.create_network" function
        '''
        
        if arg == "new":
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{self.app.tab_bar.selected_tab.name}")
            self.paquet_size_entry.delete(0, "end")
            self.paquet_size_entry.insert(0, "10")
            
            self.settings_frame.pack(expand = True, fill = "both", anchor = "center")
            self.option_frame.pack_forget()


        elif arg == "load":
            file_path = tk.filedialog.askopenfilename(title = "Gimme a save file", filetypes = (('Json File', '*.json'), ("Tous les fichiers", "*.*")))
            if not file_path:
                self.app.alert = ("Error", "NoDataFile")
                self.event_generate("<<Alert>>")
                return

            with open(file_path) as file:
                data = json.load(file)
                self.create_network(data["network_name"], data["paquet_size"])
                self.app.current_network.load_network(file_path = file_path)

        elif arg == "go_back":
            self.settings_frame.pack_forget()
            self.option_frame.pack(side = "top", fill = "both", expand = True)
        
        elif arg == "create":
            self.create_network()








class NetControls(tk.Frame):

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.network = network
        self.kwargs = kwargs
        self.icon_size : tuple = 65, 65
        self.icons : dict[str : tuple] = {
            "Next" : (load_to_size("next", *self.icon_size), load_to_size("highlight_next", *self.icon_size)),
            "Pause" : (load_to_size("pause", *self.icon_size), load_to_size("highlight_pause", *self.icon_size)),
            "Play" : (load_to_size("play", *self.icon_size), load_to_size("highlight_play", *self.icon_size)),
            }

        # Frames =======================================================================

        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", width = 5)
        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", height = 5)

        self.buffer_frame_1.pack(side = "left", fill = "both")
        self.buffer_frame_2.pack(side = "top", fill = "both")

        # Widgets ======================================================================

        self.play_button = CustomButton(self, parent_obj = self, func_arg = "play", icons = self.icons["Play"], image = self.icons["Play"][0], background = self.kwargs.get("background"))
        self.pause_button = CustomButton(self, parent_obj = self, func_arg = "pause", icons = self.icons["Pause"], image = self.icons["Pause"][0], background = self.kwargs.get("background"))
        self.go_farward = CustomButton(self, parent_obj = self, func_arg = "update", icons = self.icons["Next"], image = self.icons["Next"][0], background = self.kwargs.get("background"))

        self.set_play_button()


    def set_pause_button(self):
        self.play_button.pack_forget()

        self.go_farward.pack(side = "right", padx = 15, pady = 15)
        self.pause_button.pack(side = "right", padx = 15, pady = 15)


    def set_play_button(self):
        self.pause_button.pack_forget()

        self.go_farward.pack(side = "right", padx = 15, pady = 15)
        self.play_button.pack(side = "right", padx = 15, pady = 15)


    def passdown_func(self, arg):
        if arg == "play":
            self.set_pause_button()
            self.network.play_network()
        
        elif arg == "pause":
            self.set_play_button()
            self.network.pause_network()
        
        elif arg == "update":
            self.network.update_network()










class DataAnalysisMenu(tk.Frame):

    def __init__(self, parent, app, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.app = app
        self.kwargs = kwargs
        
        self.icon_size = 100, 100
        self.icons = {
            "Network" : load_to_size("network", *self.icon_size),
            "Compare" : load_to_size("compare", *self.icon_size),
            "Back" : (load_to_size("back", 75, 75), load_to_size("highlight_back", 75, 75))
            }

        self.data_table_tags = (
            "Name",
            "Paquet Size",
            "Paquets Created",
            "Paquets Transfered",
            "Paquets Lost",
            "Paquets Lost (%)",
            "Paquet Wait Time (Avg.)",
            "Nodes",
            "Normal Sources",
            "Buffered Sources",
            "Buffers"
            )
        
        self.data_graph_tags = (
            "Name",
            "Paquets Lost",
            "Most Connected Buffer Output"
            )

        self.network_table_data : list[dict] = self.get_network_table_data()
        self.network_graph_data : list[dict] = self.get_network_graph_data()

        # Main Frame ==================================================================

        self.main_frame = ctk.CTkScrollableFrame(self, fg_color = "#22282a", orientation = "vertical")
        self.main_frame.place(anchor = "center", relx = 0.5, rely = 0.5, relwidth = 0.6, relheight = 1)
        
        # Page Title ==================================================================

        self.title_frame = tk.Frame(self.main_frame, background = "#22282a")
        self.page_title = tk.Label(self.title_frame, image = self.icons["Compare"], compound = "left", text = "  Network Comparison", font = f"{font} 35 bold", foreground = "#FFFFFF", background = "#22282a")
        self.buffer_frame_1 = tk.Frame(self.title_frame, background = "#1D2123", height = "5")

        self.title_frame.pack(side = "top", fill = "x", padx = 20)
        self.page_title.pack(side = "top", anchor = "w", pady = 15)
        self.buffer_frame_1.pack(side = "top", fill = "x")

        # Network Data Table Frames ===================================================

        self.h_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color = "#22282a", orientation = "horizontal", height = 525)
        self.table_title = tk.Label(self.h_scroll_frame, text = "Network Data", font = f"{font} 25 bold underline", foreground = "#FFFFFF", background = "#22282a")
        self.buffer_frame_2 = tk.Frame(self.h_scroll_frame, background = "#1D2123", height = "5")
        self.table_frame = tk.Frame(self.h_scroll_frame, background = "#22282a")
        self.set_table_widgets()
        self.buffer_frame_3 = tk.Frame(self.h_scroll_frame, background = "#1D2123", height = "5")

        self.h_scroll_frame.pack(side = "top", fill = "x", padx = 20, pady = (25, 0))
        self.table_title.pack(side = "top", anchor = "w", pady = (15, 30))
        self.buffer_frame_2.pack(side = "top", fill = "x", padx = 10)
        self.table_frame.pack(side = "top")
        self.buffer_frame_3.pack(side = "top", fill = "x", padx = 10)

        # Network Graph Frames ========================================================

        self.graphs_frame = tk.Frame(self.main_frame, background = "#22282a")
        self.graphs_title = tk.Label(self.graphs_frame, text = "Network Graphs", font = f"{font} 25 bold underline", foreground = "#FFFFFF", background = "#22282a")

        self.graphs_frame.pack(side = "top", fill = "x", padx = 20, pady = (25, 0))
        self.graphs_title.pack(side = "top", anchor = "w", pady = (15, 30))
        self.set_graph_widgets()

        # Exit Controls ===============================================================

        self.back_button = CustomButton(self, parent_obj = self, func_arg = "go_back", icons = self.icons["Back"], image = self.icons["Back"][0], background = kwargs.get("background"))
        
        self.back_button.place(anchor = "nw", x = 10, y = 10)



    def get_network_table_data(self) -> None:
        data = []
        
        for network_name in self.app.network_instances:
            if network := self.app.network_instances[network_name]:
                
                paquet_loss = 0
                normal_sources = 0
                buffered_sources = 0
                buffers = 0
                
                if not network.total_paquets_transfered + network.total_paquets_lost == 0:
                    paquet_loss = round((network.total_paquets_lost / (network.total_paquets_transfered + network.total_paquets_lost)) * 100, 2)

                for node_name in network.connections:
                    node = network.nodes[node_name]
                    if node.type == "Source" and node.behaviour == "Normal":
                        normal_sources += 1
                    elif node.type == "Source" and node.behaviour == "Buffered":
                        buffered_sources += 1
                    elif node.type == "Buffer":
                        buffers += 1

                data.append({
                    "Name" : network.name,
                    "Paquet Size" : network.paquet_size,
                    "Paquets Created" : network.total_paquets_created,
                    "Paquets Transfered" : network.total_paquets_transfered,
                    "Paquets Lost" : network.total_paquets_lost,
                    "Paquets Lost (%)" : paquet_loss,
                    "Paquet Wait Time (Avg.)" : round(network.mean_paquet_wait_time, 2),
                    "Nodes" : len(network.connections),
                    "Normal Sources" : normal_sources,
                    "Buffered Sources" : buffered_sources,
                    "Buffers" : buffers
                })
        
        return data


    def get_network_graph_data(self) -> None:
        
        data = {
            "Name" : [],
            "Paquet Loss" : [],
            "Lambda" : []
            }
        
        for network_name in self.app.network_instances:

            if network := self.app.network_instances[network_name]:
                most_connected_buffer_node = None
                
                for node_name in network.connections:
                    if network.nodes[node_name].type == "Buffer":
                        
                        if most_connected_buffer_node == None:
                            most_connected_buffer_node = network.nodes[node_name]
                        elif len(network.nodes[node_name].connections) > len(most_connected_buffer_node.connections):
                            most_connected_buffer_node = network.connections[node_name]
                
                
                lambda_const = 0 if most_connected_buffer_node == None else most_connected_buffer_node.lambda_const
                paquet_loss = 0
                if not network.total_paquets_transfered + network.total_paquets_lost == 0:
                    paquet_loss = (network.total_paquets_lost / (network.total_paquets_transfered + network.total_paquets_lost)) * 100

                data["Name"].append(network.name)
                data["Paquet Loss"].append(paquet_loss)
                data["Lambda"].append(lambda_const)

        return data


    def set_table_widgets(self) -> None:
        
        buffer_offset = 1
        tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "400").grid(column = 0, row = 0, rowspan = len(self.data_table_tags), sticky = "n", padx = 10)

        for row_index, tag in enumerate(self.data_table_tags):
            tk.Label(self.table_frame, text = tag, font = f"{font} 15 bold", foreground = "#FFFFFF", background = "#22282a").grid(column = buffer_offset, row = row_index, sticky = "w")

        for colum_index, network_data in enumerate(self.network_table_data):
            tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "400").grid(column = colum_index + buffer_offset + 1, row = 0, rowspan = len(network_data), sticky = "n", padx = 10)
            buffer_offset += 1 
            for row_index, tag in enumerate(self.data_table_tags):
                if tag == "Paquet Wait Time":
                    tk.Label(self.table_frame, text = f"{network_data[tag] : 0.2f}", font = f"{font} 15 bold", foreground = "#FFFFFF", background = "#22282a").grid(column = colum_index + buffer_offset + 1, row = row_index)
                else:
                    tk.Label(self.table_frame, text = network_data[tag], font = f"{font} 15 bold", foreground = "#FFFFFF", background = "#22282a").grid(column = colum_index + buffer_offset + 1, row = row_index)
        
        tk.Frame(self.table_frame, background = "#1D2123", width = "5", height = "400").grid(column = len(self.network_table_data) + buffer_offset + 1, row = 0, rowspan = len(self.data_table_tags), sticky = "n", padx = 10)
    


    def set_graph_widgets(self) -> None:
        graph = plt.Figure(dpi = 100, facecolor = "#22282a")
        graph_canvas = FigureCanvasTkAgg(graph, self.graphs_frame)
        
        axes = graph.add_subplot(111, facecolor = "#171a1c")
        for ax in [axes.xaxis, axes.yaxis]:
            ax.set_major_locator(ticker.MaxNLocator(integer = True))
        axes.spines[["top", "right"]].set_visible(False)
        axes.spines[["bottom", "left"]].set_color("white")     
        axes.tick_params(axis = "both", colors = "white")  
        axes.set_xbound(0, None); axes.set_ybound(0, None)
        axes.set_xlabel("Lambda", color = "white")
        axes.set_ylabel("Paquet Loss (%)", color = "white")
        axes.set_xbound(lower = min(self.network_graph_data["Lambda"]) - 1, upper = max(self.network_graph_data["Lambda"]) + 1)
        axes.bar(self.network_graph_data["Lambda"], self.network_graph_data["Paquet Loss"], width = 0.8, align = "center", color = "red")    
        axes.set_ybound(lower = 0, upper = 100)
        
        rects = axes.patches
        for rect, label in zip(rects, self.network_graph_data["Name"]):
            height = rect.get_height()
            axes.text(rect.get_x() + rect.get_width() / 2, height + 2, label, ha = "center", va = "bottom", color = "white")

        graph_canvas.get_tk_widget().pack(side = "top", fill = "x", padx = 15, pady = (0, 15))
            


    def passdown_func(self, arg) -> None:
        if arg == "go_back":
            self.app.close_comparison_menu()