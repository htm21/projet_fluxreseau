# a paquet will have a predetermined path to take when it is created that coresponds to a list of node names it has pass through till its endpoint


class Paquet: # Data Class
    def __init__(self, endpoint : str, path : list[str], data : str, size : int, tracking : bool) -> None:
        
        self.endpoint : str = endpoint # Name of Endpoint Node
        self.path : list[str] = [] # precalculated path for the paquet to take
        self.data : str = data # can be anything (Symbols, Numbers etc...)
        self.size : int = size # in bits (8 bits = 1 byte)
        self.tracking : bool = tracking # if true it will show up in the GUI