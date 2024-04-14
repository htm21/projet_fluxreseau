# a paquet will have a predetermined path to take when it is created that coresponds to a list of node names it has pass through till its endpoint



class Paquet:
    def __init__(self, data : str=None, size : int=None, tracking : bool=None) -> None:
        
        self.data : str = data # peut contenir n'importe quel symbole, chiffre, ...
        self.size : int = size # en bits (8 bits = 1 byte)
        self.tracking : bool = tracking # nous permettra de mettre en avant la position actuelle du paquet dans le GUI

    def __repr__(self):
        return f"'{self.data}'" # pour représenter chaque paquet 




