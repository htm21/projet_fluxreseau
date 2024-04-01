from Modules.paquet import Paquet


class Node(object):

    instance_counter : int = 0

    def __init__(self, node_id : int, name : str, node_type : str = "Source", output_speed : int = 0, input_speed : int = 0, max_send_paquets : int = 0) -> None:
        Node.instance_counter += 1
        
        self.id : int = node_id
        self.name : str = name
        self.type : str = node_type 
        self.output_speed : int = output_speed # Bytes
        self.input_speed : int = input_speed # Bytes
        self.max_send_paquets = max_send_paquets

        self.paquet_queue : list[Paquet] = []
        self.connections : int = 0
        self.last_update_time : float = 0


    def create_paquet(self, endpoint : str = None, data : str = None, size : int = None, tracking : bool = None) -> Paquet:
        
        
        self.receve_paquet(Paquet(endpoint, data, size, tracking))
    

    def receve_paquet(self, paquet : Paquet) -> None:
        self.paquet_queue.append(paquet)


    def send_paquet(self) -> None:
        if self.paquet_queue:
            return self.paquet_queue.pop(0)


    def show_paquet_queue(self) -> list[Paquet]:
        return self.file



class Source(Node): 

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)
        Source.instance_counter += 1


    def receve_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( "'Source' object has no attribute 'receve_paquet'" )
    
    def create_paquet(self, endpoint: str = None, data: str = None, size: int = None, tracking: bool = None) -> Paquet:
        
        self.paquet_queue.append(Paquet(endpoint, data, size, tracking))



class Endpoint(Node):

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)
        
        Endpoint.instance_counter += 1


    def send_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( "'Endpoint' object has no attribute 'send_paquet'" )


    def create_paquet(self, *args, **kwargs) -> Paquet:
        raise AttributeError( "'Endpoint' object has no attribute 'cerate_paquet'" )



class Buffer(Node):

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)

        Buffer.instance_counter += 1
        
        self.capacity = 10  # Comme ce buffer est de capacité finie, notée C ici je prends 10 pour l'exemple
        self.number_element = 0
        self.file = []


    def receve_paquet(self, paquet : Paquet) -> None:
        if self.number_element < self.capacity :
            self.file.append(paquet)
            self.number_element += 1
        else:
            del paquet


    def send_paquet(self) -> Paquet:
        if self.number_element :
            return self.file.pop(0)       


    def create_paquet(self, *args, **kwargs) -> Paquet:
        raise AttributeError( "'Buffer' object has no attribute 'cerate_paquet'" )