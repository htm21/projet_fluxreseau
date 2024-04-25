import ctypes
import platform
import tkinter as tk

from time import time
from Modules.app import App



def main() -> None:

    # Ignore la mise à l'échelle de l'écran des système d'exploitation "Windows" afin que les widgets de l'interface graphique n'apparaissent pas trop gros à l'écran (en général pour les widgets contenant du texte)
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)


    # On intialise la fenêtre tkinter et on la passe en argument dans l'instance "app" de la class App pour la gérée 
    root = tk.Tk()
    app  = App(root)


    # app.Running est réglé sur « True » au démarrage et arrêtera toutes les mises à jour et fonctions de l'interface graphique et de la logique s'il est réglé sur « False ».
    while app.Running:

        # try-else permettant de détecter les éventuels bugs
        try:
            
            # MAJ du réseau actuel sélectionné (app.current_network)
            # à condition que ce Network ne soit pas en état "pause" et que le temps écouler depuis la dernière mise à jour soit inférieur ou égale au temps pour la MAJ
            if not app.current_network.pause and (time() - app.current_network.last_updated) >= app.update_speed:
                app.current_network.update_network()
            
            # Vérifie s'il y a une alerte utilisateur à l'écran, et si son temps d'affichage est écoulé
            if app.alert_lable.winfo_ismapped():
                if (time() - app.alert_create_time) > app.alert_on_screen_time:
                    app.alert_lable.place_forget()
            
            # Si un object est selectionné par l'utilisateur, ses informations seront affiché sur le menu latéral "Sidebar"
            # MAJ de manière continue
            # (None == Network object)
            if obj := app.current_network.selected_node:
                app.side_bar.set_object_info(obj)
            else:
                app.side_bar.set_object_info(app.current_network)
        
        except: 
            pass
        
        # Utilisation de update au lieu de mainloop pour ne pas rester bloqué dans une boucle
        root.update()



if __name__ == "__main__":
    # Clear Terminal au Start (pour debug)
    print("\033c")
    main()
