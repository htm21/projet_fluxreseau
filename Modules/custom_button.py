import tkinter as tk


class CustomButton(tk.Label):
    def __init__(self, parent, event = None, *args, **kwargs) -> None:
        tk.Label.__init__(self, parent, *args, kwargs)
        self.parent = parent
        self.event = event
        self.kwargs = kwargs


        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_click(self, *args):
        self.event_generate(self.event)

    def on_enter(self, *args) -> None:
        self.config(foreground = "#ffcc22")
    
    def on_leave(self, *args) -> None:
        self.config(foreground = self.kwargs.get("foreground"))