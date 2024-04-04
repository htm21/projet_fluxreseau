import ctypes
import platform
import tkinter as tk

from time import time
from Modules.app import App


def main() -> None:
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)

    root = tk.Tk()
    app  = App(root)


    app.network_sandbox.test()
    # while app:
        
    #     try:
            
    #         if app.alert_lable.winfo_ismapped():
    #             if (time() - app.alert_create_time) > app.alert_on_screen_time:
    #                 app.alert_lable.place_forget()
            
    #         if obj := app.network_sandbox.selected_node: # to be moved into the update function
    #             app.side_bar.set_object_info(obj)
    #         else:
    #             app.side_bar.set_object_info(app.network_sandbox)
        
    #     except: 
    #         pass
        
    #     root.update()


if __name__ == "__main__":
    print("\033c") # Clear Terminal at Start 
    main()