from time import time


class Paquet:
    '''
    Paquet est une class de données contenant trois éléments d’information :
    - données (aléatoires)
    - taille des données 
    - moment de la création (utilisé pour calculer les temps d’attente des paquets dans les Buffers) 
    '''
    def __init__(self, data : str = None, size : int = None) -> None:
        
        self.data : str = data      # peut contenir n'importe quel symbole, chiffre, ...
        self.size : int = size      
        self.creation_time : float = time()


    def __repr__(self):
        return f"{self.data}" # pour représenter chaque paquet 




