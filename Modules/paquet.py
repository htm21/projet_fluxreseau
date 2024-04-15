


class Paquet:
    '''
    The "Paquet" class is a data class that represents Data that "Node" objects are able to manipulate.
    A "Paquet" object can be seen on the GUI through the "SideBar" (Node Info) or it will Highlight nodes if "tracking" is set to "True"
    '''

    def __init__(self, endpoint : str = None, data : str = None, size : int = None, tracking : bool = None) -> None:
        
        self.endpoint : str = endpoint # Name of Endpoint Node
        self.data : str = data # can be anything (Symbols, Numbers etc...)
        self.size : int = size
        self.tracking : bool = tracking # if true it will show up in the GUI

    def __repr__(self) -> str:
        return f"'{self.data}'"