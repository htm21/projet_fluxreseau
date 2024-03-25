import tkinter as tk


class CustomButton(tk.Label):
    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Label.__init__(self, parent, *args, kwargs)
        self.parent = parent
        self.kwargs = kwargs

        # self.active_foreground = "#ffcc22"
        # self.inactive_foreground = kwargs.get("foreground")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)



    def on_enter(self, *args) -> None:
        self.config(foreground = "#ffcc22")
    
    def on_leave(self, *args) -> None:
        self.config(foreground = self.kwargs.get("foreground"))