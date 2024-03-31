import ctypes
import platform
import tkinter as tk

from Modules.app import App


def main() -> None:

    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)

    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    print("\033c") # Clear Terminal at Start 
    main()