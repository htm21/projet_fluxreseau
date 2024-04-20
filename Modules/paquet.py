from time import time


class Paquet:
    def __init__(self, data : str = None, size : int = None, tracking : bool = None) -> None:
        
        self.data : str = data # peut contenir n'importe quel symbole, chiffre, ...
        self.size : int = size
        self.creation_time : float = time()
        self.tracking : bool = tracking # nous permettra de mettre en avant la position actuelle du paquet dans le GUI

    def __repr__(self):
        return f"'{self.data}'" # pour représenter chaque paquet 




