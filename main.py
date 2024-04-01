import ctypes
import platform
import tkinter as tk

from Modules.app import App


def main() -> None:

    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)

    root = tk.Tk()
    app = App(root)

    app.network_sandbox.add_node("Source", "TEST S")
    app.network_sandbox.add_node("Buffer", "TEST B")
    app.network_sandbox.create_link("TEST S", "TEST B")
    app.network_sandbox.update_network()


    #root.mainloop()


if __name__ == "__main__":
    print("\033c") # Clear Terminal at Start 
    main()