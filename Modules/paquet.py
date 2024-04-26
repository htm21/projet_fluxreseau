from time import time


class Paquet:
    '''
    Paquet is a data class containing 3 pieces of information:
    - data (random)
    - data size 
    - ceration time (used to calculate paquet wait times in the buffers) 
    '''
    def __init__(self, data : str = None, size : int = None) -> None:
        
        self.data : str = data      # peut contenir n'importe quel symbole, chiffre, ...
        self.size : int = size      
        self.creation_time : float = time()


    def __repr__(self):
        return f"{self.data}" # pour représenter chaque paquet 




