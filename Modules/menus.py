import tkinter as tk

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
        
        self.node_type_lable = tk.Label(self.type_frame, text = "Node Type :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.node_class_label = tk.Label(self.type_frame, font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.name_label = tk.Label(self.name_frame, text = "Node Name :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.name_entry = tk.Entry(self.name_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.output_speed_label = tk.Label(self.output_speed_frame, text = "Output Speed (Bytes) :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.output_speed_entry = tk.Entry(self.output_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.input_speed_label = tk.Label(self.input_speed_frame, text = "Input Speed (Bytes) :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.input_speed_entry = tk.Entry(self.input_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.send_paquets_label = tk.Label(self.send_paquets_frame, text = "Send Paquets :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.send_paquets_entry = tk.Entry(self.send_paquets_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.lambda_setting_label = tk.Label(self.lambda_setting_frame, text = "Lambda :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
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

        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def cancel_node(self, *args):
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
        self.input_speed_entry.insert(0, "1000000")
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
            self.output_speed_entry.insert(0, "100000000")
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
            self.output_speed_entry.insert(0, "1500000")
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
        self.delete_button = tk.Button(self.controls, image = self.icons["Delete"], compound = "left", justify = "left", text = "  Delete", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#4d0000", activebackground = "#4d0000", highlightbackground = "#ffcc22", relief = "sunken", border = 0, command = self.delete_network)
        self.cancel_button = tk.Button(self.controls, image = self.icons["Success"], compound = "left", justify = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#004d00", activebackground = "#004d00", highlightbackground = "#ffcc22", relief = "sunken", border = 0, command = self.cancel_deletion)

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

    def __init__(self, parent, network, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        PaquetCreationMenu.instance_counter += 1

        self.icon_size = 75, 75
        self.icons = {
            "Paquet" : (load_to_size("paquet", *self.icon_size), load_to_size("highlighted_paquet", *self.icon_size))
            }
        

        self.data_lable = tk.Label(self.settings, text = "Paquet Data (Mb)",font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.size_lable = tk.Label(self.settings, text = "",font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.endpoint_lable = tk.Label(self.settings, text = "",font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.tracking_lable = tk.Label(self.settings, text = "",font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

    def create_paquet(self, *args) -> None:
        PaquetCreationMenu.instance_counter -= 1
        
        self.node.create_paquet(endpoint = None, data = None, size = None, tracking = None)
        self.destroy()


    def cancel_creation(self, *args) -> None:
        PaquetCreationMenu.instance_counter -= 1
        self.destroy()


    def on_enter(self, button):
        button.config(foreground = "#ffcc22")


    def on_leave(self, button):
        button.config(foreground = "#FFFFFF")

