import tkinter as tk

from Modules.node import Node, Source, Buffer, Endpoint
from Modules.custom_button import CustomButton 
from Modules.utils import *

class NodeCreationMenu(tk.Frame):

    instance_counter = 0

    def __init__(self, parent, parent_obj, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        NodeCreationMenu.instance_counter += 1

        self.parent = parent
        self.parent_obj = parent_obj

        self.NODE_TYPES : dict[str : Node]= {
            "Source" : Source,
            "Endpoint" : Endpoint,
            "Buffer" : Buffer,
            "Node" : Node
            }
        
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
        self.max_paquets_frame = tk.Frame(self.node_settings, background = kwargs.get("background"))
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
        
        self.type_label = tk.Label(self.type_frame, text = "Node Type :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.node_type = tk.Label(self.type_frame, font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.name_label = tk.Label(self.name_frame, text = "Node Name :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.name_entry = tk.Entry(self.name_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.output_speed_label = tk.Label(self.output_speed_frame, text = "Output Speed (Bytes) :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.output_speed_entry = tk.Entry(self.output_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.input_speed_label = tk.Label(self.input_speed_frame, text = "Input Speed (Bytes) :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.input_speed_entry = tk.Entry(self.input_speed_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.max_paquets_label = tk.Label(self.max_paquets_frame, text = "Max Paquets :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.max_paquets_entry = tk.Entry(self.max_paquets_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)
        
        self.lambda_setting_label = tk.Label(self.lambda_setting_frame, text = "Lambda :", font = f"{font} 25 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.lambda_setting_entry = tk.Entry(self.lambda_setting_frame, font = f"{font} 18 bold", foreground = "#FFFFFF", background = "#171a1c", borderwidth = 0, selectborderwidth = 0)

        self.create_button = tk.Button(self.controls, image = self.icons["Success"], compound = "left", justify = "left", text = "  Create", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#004d00", activebackground = "#004d00", relief = "sunken", border = 0, command = self.create_node)
        self.cancel_button = tk.Button(self.controls, image = self.icons["Error"], compound = "left", justify = "left", text = "  Cancel", font = f"{font} 25 bold", foreground = "#FFFFFF", activeforeground = "#ffcc22", background = "#4d0000", activebackground = "#4d0000", relief = "sunken", border = 0, command = self.cancel_node)


        self.choose_node_lable.pack(anchor = "center", fill = "x", expand = True)
        
        self.source_choice.pack(side = "left", fill = "x", expand = True)
        self.endpoint_choice.pack(side = "left", fill = "x", expand = True)
        self.buffer_choice.pack(side = "left", fill = "x", expand = True)
        
        self.type_label.pack(side = "left")
        self.node_type.pack(side = "right")

        self.name_label.pack(side = "left")
        self.name_entry.pack(side = "right")
        
        self.output_speed_label.pack(side = "left")
        self.output_speed_entry.pack(side = "right")
        
        self.input_speed_label.pack(side = "left")
        self.input_speed_entry.pack(side = "right")
        
        self.max_paquets_label.pack(side = "left")
        self.max_paquets_entry.pack(side = "right")
        
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
        self.parent_obj.add_node()
        # pass
        NodeCreationMenu.instance_counter -= 1
        self.destroy()
    
    def cancel_node(self, *args):
        NodeCreationMenu.instance_counter -= 1
        self.destroy()


    def reset_settings(self):
        self.type_frame.pack_forget()
        self.choose_node_lable.pack_forget()
        self.name_frame.pack_forget()
        self.output_speed_frame.pack_forget()
        self.input_speed_frame.pack_forget()
        self.max_paquets_frame.pack_forget()
        self.lambda_setting_frame.pack_forget()


    def passdown_func(self, arg):
        
        self.reset_settings()

        self.type_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        self.name_frame.pack(padx = 20, pady = 10, fill = "x", expand = True)
        
        if arg == "Source":
            self.node_type.config(text = arg, foreground = "#354d33")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{self.NODE_TYPES[arg].instance_counter}")
            self.output_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.max_paquets_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
        
        elif arg == "Endpoint":
            self.node_type.config(text = arg, foreground = "#3d2932")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{self.NODE_TYPES[arg].instance_counter}")
            self.input_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.lambda_setting_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
        
        elif arg == "Buffer":
            self.node_type.config(text = arg, foreground = "#3d3829")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, f"{arg}-{self.NODE_TYPES[arg].instance_counter}")
            self.output_speed_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)
            self.lambda_setting_frame.pack(padx = 20, pady = 10,fill = "x", expand = True)

        self.node_settings.pack(side = "top", fill = "x", padx = 20, pady = 20)