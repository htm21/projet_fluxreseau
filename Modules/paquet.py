# a paquet will have a predetermined path to take when it is created that coresponds to a list of node names it has pass through till its endpoint



class Paquet:
    def __init__(self, endpoint : str=None, data : str=None, size : int=None, tracking : bool=None) -> None:
        
        self.endpoint : str = endpoint # Name of Endpoint Node
        self.data : str = data # can be anything (Symbols, Numbers etc...)
        self.size : int = size # in bits (8 bits = 1 byte)
        self.tracking : bool = tracking # if true it will show up in the GUI