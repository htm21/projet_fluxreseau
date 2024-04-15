import ctypes
import platform
import tkinter as tk

from Modules.menus import NewNetworkMenu
from time import time
from Modules.app import App


def main() -> None:
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)

    root = tk.Tk()
    app  = App(root)


    while app.Running:
        
        try:

            if not app.current_network.pause and (time() - app.current_network.last_updated) >= app.current_network.update_speed:
                app.current_network.update_network()
            
            if app.alert_lable.winfo_ismapped():
                if (time() - app.alert_create_time) > app.alert_on_screen_time:
                    app.alert_lable.place_forget()
            
            if obj := app.current_network.selected_node:
                app.side_bar.set_object_info(obj)
            else:
                app.side_bar.set_object_info(app.network_sandbox)
        
        except: 
            pass
        
        root.update()

    # root.mainloop()


if __name__ == "__main__":
    print("\033c") # Clear Terminal at Start 
    main()