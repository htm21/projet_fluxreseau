from Modules.paquet import Paquet



class Node(object):

    _instance_counter = 0

    def __init__(self, name, node_type, oputput_speed = None) -> None:
        Node._instance_counter += 1
        
        self.name : str = name
        self.type : str = node_type
        self.oputput_speed : int = oputput_speed
        self.data_paquets : list = []


    def send_paquet(self, data, size, enpoint = None) -> Paquet:
        return Paquet(data, size, enpoint)
    
    
    def receve_paquet(self, paquet : Paquet) -> None:
        self.data_paquets.append(paquet)



class Source(Node): 

    _instance_counter = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        Source._instance_counter += 1


    def receve_paquet(self) -> AttributeError:
        raise AttributeError( "'Source' object has no attribute 'receve_paquet'" )



class Endpoint(Node):

    _instance_counter = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        Endpoint._instance_counter += 1


    def send_paquet(self) -> AttributeError:
        raise AttributeError( "'Endpoint' object has no attribute 'send_paquet'" )



class Buffer(Node):
# Modify to be able to create it from the network class
    
    def __init__(self) -> None: 
        self.file : list[Paquet] = []
        self.capacity = 10      # Comme ce buffer est de capacité finie, notée C ici je prends 10 pour l'exemple
        self.number_element = 0
    
    def enfiler(self, paquet : Paquet) -> None:
        if self.number_element < self.capacity :
            self.file.append(paquet)
            self.number_element += 1

    def defiler(self) -> Paquet:
        if self.number_element > 0 :
            element = self.file.pop(0)       
        return element

    def afficher_file(self) -> list:
        return self.file