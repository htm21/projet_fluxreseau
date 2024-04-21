import ctypes
import platform
import tkinter as tk

from time import time
from Modules.app import App



def main() -> None:

    # Ignores Windows Screen Scaling so the GUI widgets don't look blown out on screen
    # This is mostly for any widgets that contain text
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)


    # Here we initialize the tkinter window and pass it onto the App class where it will be managed 
    root = tk.Tk()
    app  = App(root)


    # app.Running is set to "True" at start and will stop all GUI & Logic updates and functions when set to "False"
    while app.Running:

        # try-else statement to catch any bugs
        try:
            
            # Here we update the current network that is selected
            if not app.current_network.pause and (time() - app.current_network.last_updated) >= app.update_speed:
                app.current_network.update_network()
            
            # Check if there is a user alert is on screen, and if its display time is up
            if app.alert_lable.winfo_ismapped():
                if (time() - app.alert_create_time) > app.alert_on_screen_time:
                    app.alert_lable.place_forget()
            
            # If a object is selected on the network, the object's info is shown onto the "Sidebar"
            # It is updated regularly to show real time info 
            # (None == Network object)
            if obj := app.current_network.selected_node:
                app.side_bar.set_object_info(obj)
            else:
                app.side_bar.set_object_info(app.current_network)
        
        except: 
            pass
        
        # Use of update instead of mainloop to not get stuck in a loop
        root.update()



if __name__ == "__main__":
    # Clear Terminal at Start (for debug)
    print("\033c")
    main()
