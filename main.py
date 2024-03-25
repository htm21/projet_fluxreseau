import time
import Modules.utils
from Modules.network import Network
from Modules.paquet import Paquet
from Modules.node import Node, Source, Buffer, Endpoint

import sys
import ctypes
import tkinter as tk
from GUIModules.app import App


def main() -> None:

    if "win" in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(0)


    root = tk.Tk()

    app = App(root)
    

    root.mainloop()


    network = Network()

    # network.add_node(node_type = "Source")
    # network.add_node(node_type = "Buffer")
    # network.add_node(node_type = "Endpoint")
    # # network.add_node()

    # network.create_link("Source-0", "Buffer-0")
    # network.create_link("Buffer-0", "Endpoint-0")
    # # network.create_link("Node-3", "Source-0")

    # network.info()

if __name__ == "__main__":
    print("\033c") # Clear Terminal Start
    main()
