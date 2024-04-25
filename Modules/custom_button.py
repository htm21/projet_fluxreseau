import tkinter as tk


class CustomButton(tk.Label):               # Initialisation de la class CustomButton, modélisant les boutons, hérite de l'objet Frame de tkinter
    def __init__(self, parent, event = None, parent_obj = None, func_arg = None, icons = [], *args, **kwargs) -> None:
        tk.Label.__init__(self, parent, *args, kwargs)
        
        self.kwargs = kwargs
        self.icons = icons                  # Association de l'icône correspondante au bouton
        self.event = event                  # Association à l'événement associé au bouton
        self.parent_obj = parent_obj
        self.func_arg = func_arg

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)


    def on_click(self, *args):
        """ Fonction qui permet la mise en marche de l'événement associé au bouton (s'active quand celui si est cliqué) """
        if self.event:
            self.event_generate(self.event)
        
        if self.parent_obj and self.func_arg:
            self.parent_obj.passdown_func(self.func_arg)


    def on_enter(self, *args) -> None:
        if len(self.icons) == 2:
            self.config(foreground = "#ffcc22", image = self.icons[1])
        self.config(foreground = "#ffcc22")


    def on_leave(self, *args) -> None:
        if len(self.icons) == 2:
            self.config(foreground = "#ffcc22", image = self.icons[0])
        self.config(foreground = self.kwargs.get("foreground"))