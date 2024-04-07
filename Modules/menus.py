import tkinter as tk
import customtkinter as ctk
 
from Modules.node import Node, Source, Buffer, Endpoint
from Modules.custom_button import CustomButton 
from Modules.utils import *



class NodeCreationMenu(tk.Frame):

    instance_counter = 0

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        NodeCreationMenu.instance_counter += 1

        self.network = network
        
        self.icon_size : tuple = 75, 75
        self.icons : dict[str : tuple] = {
            "Node" : (load_to_size("node", *self.icon_size), load_to_size("highlight_node", *self.icon_size)),
            "Source" : (load_to_size("source_node", *self.icon_size), load_to_size("highlight_source_node", *self.icon_size)),
            "Buffer" : (load_to_size("buffer_node", *self.icon_size), load_to_size("highlight_buffer_node", *self.icon_size)),
            "Endpoint" : (load_to_size("endpoint_node", *self.icon_size), load_to_size("highlight_endpoint_node", *self.icon_size)),
            "Success" : load_to_size("success", 35, 35),
            "Error" : load_to_size("error", 35, 35)
            } # dictionary that holds the normal node image and also the highlighted node image


        # Frames =======================================================================

        self.node_choice = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.node_settings = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))

        self.type_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.name_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.output_speed_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.input_speed_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.send_paquets_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
        self.lambda_setting_frame = tk.Frame(self.node_settings, background = kwargs.get("background")) 


        self.node_choice.pack(side = "top", fill = "x", padx = 20, pady = 20)
        self.buffer_frame1.pack(side = "top", fill = "x")
        self.node_settings.pack(side = "top", fill = "both", expand = True, padx = 20, pady = 20)
        self.buffer_frame2.pack(side = "top", fill = "x")
        self.controls.pack(side = "top", fill = "x", padx = 20, pady = 20)
        
        
        # Widgets ======================================================================

        self.choose_node_lable = tk.Label(self.node_settings, text = "Choose A Node", font = f"{font} 40 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.source_choice = CustomButton(self.node_choice, parent_obj = self, func_arg = "Source", image = self.icons["Source"][0], icons = self.icons["Source"], text = "Source Node", compound = "top", font = f"{font} 18 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.endpoint_choice = CustomButton(self.node_choice, parent_obj = self, func_arg = "Endpoint", image = self.icons["Endpoint"][0], icons = self.icons["Endpoint"], text = "Endpoint Node", compound = "top", font = f"{font} 18 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.buffer_choice = CustomButton(self.node_choice, parent_obj = self, func_arg = "Buffer", image = self.icons["Buffer"][0], icons = self.icons["Buffer"], text = "Buffer Node", compound = "top", font = f"{font} 18 bold", foreground = "#FFFFFF", background = kwargs.get("background")) 
        
        self.node_type_lable = tk.Label(self.type_frame, text = "Type : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.node_class_label = tk.Label(self.type_frame, font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.name_label = tk.Label(self.name_frame, text = "Name : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.name_entry = tk.Entry(self.name_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.output_speed_label = tk.Label(self.output_speed_frame, text = "Output : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.output_speed_entry = tk.Entry(self.output_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.input_speed_label = tk.Label(self.input_speed_frame, text = "Throughput : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.input_speed_entry = tk.Entry(self.input_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.send_paquets_label = tk.Label(self.send_paquets_frame, text = "Send Paquets : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.send_paquets_entry = tk.Entry(self.send_paquets_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.lambda_setting_label = tk.Label(self.lambda_setting_frame, text = "Lambda : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.lambda_setting_entry = tk.Entry(self.lambda_setting_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)

        self.create_button = tk.Button(self.controls, image = self.icons["Success"], compound = "left", justify = "left", text = "  Create", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#004d00", activebackground = "#004d00", relief = "sunken", border = 0, command = self.create_node)
        self.cancel_button = tk.Button(self.controls, image = self.icons["Error"], compound = "left", justify = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#4d0000", activebackground = "#4d0000", relief = "sunken", border = 0, command = self.cancel_node)


        self.choose_node_lable.pack(anchor = "center", fill = "x", expand = True)
        
        self.source_choice.pack(side = "left", fill = "x", expand = True)
        self.endpoint_choice.pack(side = "left", fill = "x", expand = True)
        self.buffer_choice.pack(side = "left", fill = "x", expand = True)
        
        self.node_type_lable.pack(side = "left")
        self.node_class_label.pack(side = "right")

        self.name_label.pack(side = "left")
        self.name_entry.pack(side = "right")
        
        self.output_speed_label.pack(side = "left")
        self.output_speed_entry.pack(side = "right")
        
        self.input_speed_label.pack(side = "left")
        self.input_speed_entry.pack(side = "right")
        
        self.send_paquets_label.pack(side = "left")
        self.send_paquets_entry.pack(side = "right")
        
        self.lambda_setting_label.pack(side = "left")
        self.lambda_setting_entry.pack(side = "right")

        self.create_button.pack(side = "right", padx = (50, 10), ipadx = 15)
        self.cancel_button.pack(side = "right", ipadx = 15)

        # Binds ======================================================================

        self.create_button.bind("<Enter>", lambda args, button = self.create_button: self.on_enter(button))
        self.create_button.bind("<Leave>", lambda args, button = self.create_button: self.on_leave(button))
        self.cancel_button.bind("<Enter>", lambda args, button = self.cancel_button: self.on_enter(button))
        self.cancel_button.bind("<Leave>", lambda args, button = self.cancel_button: self.on_leave(button))


    def on_enter(self, button):
        button.config(foreground = "#ffcc22")


    def on_leave(self, button):
        button.config(foreground = "#FFFFFF")


    def create_node(self, *args):
        
        node_type = self.node_class_label.cget("text")

        if not node_type: return

        name = self.name_entry.get()
        output_speed = 0
        input_speed = 0
        send_paquets = 0

        if node_type == "Source":
            output_speed = int(self.output_speed_entry.get()) if int(self.output_speed_entry.get()) >= 0 else 0
            send_paquets = int(self.send_paquets_entry.get())

        elif node_type == "Endpoint":
            input_speed = int(self.input_speed_entry.get()) if int(self.input_speed_entry.get()) >= 0 else 0

        elif node_type == "Buffer":
            output_speed = int(self.output_speed_entry.get()) if int(self.output_speed_entry.get()) >= 0 else 0
        
        self.network.add_node(node_type = node_type, name = name, output_speed = output_speed, input_speed = input_speed, max_send_paquets = send_paquets)
        # === === === === Lambda setting is not passed to node creation yet === === === ===

        self.network.net_controls.place(anchor = "nw", x = 0, y = 0)
        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def cancel_node(self, *args):
        self.network.net_controls.place(anchor = "nw", x = 0, y = 0)
        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def reset_settings(self) -> None:
        
        # Frames ======================================
        self.type_frame.pack_forget()
        self.choose_node_lable.pack_forget()
        self.name_frame.pack_forget()
        self.output_speed_frame.pack_forget()
        self.input_speed_frame.pack_forget()
        self.send_paquets_frame.pack_forget()
        self.lambda_setting_frame.pack_forget()
        
        # Widgets ======================================
        self.output_speed_entry.delete(0, "end")
        self.input_speed_entry.delete(0, "end")
        self.input_speed_entry.insert(0, "10")
        self.send_paquets_entry.delete(0, "end")
        self.lambda_setting_entry.delete(0, "end")
        self.lambda_setting_entry.insert(0, "0")


    def passdown_func(self, arg):
        
        self.reset_settings()

        self.type_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        self.name_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        

        if arg == "Source":
            self.node_class_label.config(text = arg, foreground = "#354d33")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{NODE_TYPES[arg].instance_counter + 1}")
            self.output_speed_entry.insert(0, "100")
            self.send_paquets_entry.insert(0, "0")
            self.output_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.send_paquets_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
        
        elif arg == "Endpoint":
            self.node_class_label.config(text = arg, foreground = "#3d2932")
            
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{NODE_TYPES[arg].instance_counter + 1}")
            self.input_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.lambda_setting_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
        
        elif arg == "Buffer":
            self.node_class_label.config(text = arg, foreground = "#3d3829")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{NODE_TYPES[arg].instance_counter + 1}")
            self.output_speed_entry.insert(0, "50")
            self.output_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.lambda_setting_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)

        self.node_settings.pack(side = "top", fill = "x", padx = 20, pady = 20)




















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
            "Network" : load_to_size("network", *self.icon_size),
            "Delete" : (load_to_size("delete", 35, 35)),
            "Success" : load_to_size("success", 35, 35),
            "Error" : load_to_size("error", 35, 35)
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
        self.delete_button = tk.Button(self.controls, image = self.icons["Delete"], compound = "left", justify = "left", text = "  Delete", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#4d0000", activebackground = "#4d0000", relief = "sunken", border = 0, command = self.delete_network)
        self.cancel_button = tk.Button(self.controls, justify = "left", text = "Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#004d00", activebackground = "#004d00", relief = "sunken", border = 0, command = self.cancel_deletion)

        self.info_label.pack(side = "top", pady = (20, 0))
        self.confirmation_label.pack(side = "top", pady = 20)
        self.delete_button.pack(side = "right", expand = True, ipadx = 15)
        self.cancel_button.pack(side = "right", expand = True, ipadx = 15)

        # Binds ======================================================================

        self.delete_button.bind("<Enter>", lambda args, button = self.delete_button: self.on_enter(button))
        self.delete_button.bind("<Leave>", lambda args, button = self.delete_button: self.on_leave(button))
        self.cancel_button.bind("<Enter>", lambda args, button = self.cancel_button: self.on_enter(button))
        self.cancel_button.bind("<Leave>", lambda args, button = self.cancel_button: self.on_leave(button))


    def delete_network(self, *args) -> None:
        DelNetMenu.instance_counter -= 1

        self.network.delete_network()
        self.destroy()


    def cancel_deletion(self, *args) -> None:
        DelNetMenu.instance_counter -= 1
        self.destroy()

    def on_enter(self, button):
        button.config(foreground = "#ffcc22")


    def on_leave(self, button):
        button.config(foreground = "#FFFFFF")





















class PaquetCreationMenu(tk.Frame):
    
    instance_counter = 0

    def __init__(self, parent, node : Node, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        PaquetCreationMenu.instance_counter += 1

        self.node = node
        self.network = network
        self.icon_size = 75, 75
        self.icons = {
            "Paquet" : load_to_size("paquet", *self.icon_size),
            "Success" : load_to_size("success", 35, 35),
            "Error" : load_to_size("error", 35, 35)
            }
        self.endpoint_nodes = self.get_all_endpoints()
        self.endpoint = set()


        # Frames =======================================================================

        self.window_title_frame = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.paquet_settings = tk.Frame(self, background = kwargs.get("background"))
        self.buffer_frame2 = tk.Frame(self, background = "#1D2123", height = 5)
        self.controls = tk.Frame(self, background = kwargs.get("background"))

        self.data_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 
        self.size_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 
        self.endpoint_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 
        self.tracking_frame = tk.Frame(self.paquet_settings, background = kwargs.get("background")) 

        self.window_title_frame.pack(side = "top", fill = "x", padx = 20, pady = 20)
        self.buffer_frame1.pack(side = "top", fill = "x")
        self.paquet_settings.pack(side = "top", fill = "x", expand = True, padx = 20, pady = 20)
        self.buffer_frame2.pack(side = "top", fill = "x")
        self.controls.pack(side = "top", fill = "x", padx = 20, pady = 20)

        self.data_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        self.size_frame.pack(padx = 20, pady = 10, fill = "x")
        self.endpoint_frame.pack(padx = 20, pady = 10, fill = "x")
        self.tracking_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)

        # Widgets ======================================================================

        self.window_title = tk.Label(self.window_title_frame, image = self.icons["Paquet"], compound = "left", justify = "right", text = "  Paquet Creation", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.data_lable = tk.Label(self.data_frame, text = "Data : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.data_entry = tk.Entry(self.data_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        self.data_entry.insert(0, f"Hello from {self.node.name}")

        self.size_lable = tk.Label(self.size_frame, text = "Data Size (Mb) : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.size_entry = tk.Entry(self.size_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        self.size_entry.insert(0, "10")

        self.endpoint_lable = tk.Label(self.endpoint_frame, text = "Endpoint : ", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.endpoint_dropdown = ctk.CTkComboBox(self.endpoint_frame, state = "readonly", width = 323, height = 40, corner_radius = 0, border_width = 0, font = (f"{font} bold", 20), dropdown_font = (f"{font} bold", 15), text_color = "#FFFFFF", fg_color = "#171a1c", border_color = "#171a1c", button_hover_color = "#ffcc22", values = self.endpoint_nodes)
        self.endpoint_dropdown.set(self.endpoint_nodes[0])

        self.tracking_lable = tk.Label(self.tracking_frame, text = "Tracking : ",font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.tracking_checkbox = ctk.CTkCheckBox(self.tracking_frame, width = 0, height = 0, checkbox_width = 40, checkbox_height = 40, text = None, corner_radius = 0, hover = False, checkmark_color = "#ffcc22", bg_color = kwargs.get("background"), fg_color = kwargs.get("background"), border_color = "#1D2123")

        self.create_button = tk.Button(self.controls, image = self.icons["Success"], compound = "left", justify = "left", text = "  Create", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#004d00", activebackground = "#004d00", relief = "sunken", border = 0, command = self.create_paquet)
        self.cancel_button = tk.Button(self.controls, image = self.icons["Error"], compound = "left", justify = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#4d0000", activebackground = "#4d0000", relief = "sunken", border = 0, command = self.cancel_paquet)


        self.window_title.pack(side = "left")

        self.data_lable.pack(side = "left")
        self.data_entry.pack(side = "right")
        
        self.size_lable.pack(side = "left")
        self.size_entry.pack(side = "right")
        
        self.endpoint_lable.pack(side = "left")
        self.endpoint_dropdown.pack(side = "right")
        
        self.tracking_lable.pack(side = "left")
        self.tracking_checkbox.pack(side = "right")
        
        self.create_button.pack(side = "right", padx = (50, 10), ipadx = 15)
        self.cancel_button.pack(side = "right", ipadx = 15)


        # Binds ======================================================================

        self.create_button.bind("<Enter>", lambda args, button = self.create_button: self.on_enter(button))
        self.create_button.bind("<Leave>", lambda args, button = self.create_button: self.on_leave(button))
        self.cancel_button.bind("<Enter>", lambda args, button = self.cancel_button: self.on_enter(button))
        self.cancel_button.bind("<Leave>", lambda args, button = self.cancel_button: self.on_leave(button))


    def get_all_endpoints(self):
        endpoint_nodes = []      
        for node_name in self.network.connections:
            if self.network.nodes[node_name].type == "Endpoint":
                endpoint_nodes.append(node_name)
        return endpoint_nodes


    def create_paquet(self, *args) -> None:
        data = self.data_entry.get()
        size = float(self.size_entry.get()) if float(self.size_entry.get()) >= 0 else 0
        endpoint = self.endpoint_dropdown.get()
        tracking = self.tracking_checkbox.get()
        self.node.create_paquet(endpoint = endpoint, data = data, size = size, tracking = tracking)
        
        self.network.net_controls.place(anchor = "nw", x = 0, y = 0)
        PaquetCreationMenu.instance_counter -= 1
        self.destroy()


    def cancel_paquet(self, *args) -> None:
        self.network.net_controls.place(anchor = "nw", x = 0, y = 0)
        PaquetCreationMenu.instance_counter -= 1
        self.destroy()


    def on_enter(self, button):
        button.config(foreground = "#ffcc22")


    def on_leave(self, button):
        button.config(foreground = "#FFFFFF")













class AppInfoMenu(tk.Frame):
    
    instance_counter = 0
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        PaquetCreationMenu.instance_counter += 1


        self.info_book = ctk.CTkTabview(self, bg_color = "#171a1c", fg_color = "#22282a")
        
        self.info_book.add("Nodes")
        self.info_book.add("Connections")
        self.info_book.add("Side Bar")
        self.info_book.add("Save Files")
        
        self.node_tab = tk.Frame(self.info_book.tab("Nodes"), background = "#FF0000")
        self.connection_tab = tk.Frame(self.info_book.tab("Connections"), background = "#00FF00")
        self.sidebar_tab = tk.Frame(self.info_book.tab("Side Bar"), background = "#0000FF")
        self.save_files_tab = tk.Frame(self.info_book.tab("Save Files"), background = "#FF00FF")
        


        self.info_book.pack(fill = "both", expand = True)