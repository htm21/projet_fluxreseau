from Modules.paquet import Paquet


class Node(object):

    instance_counter : int = 0

    def __init__(self, node_id : int, name : str, node_type : str = "Source", output_speed : int = 0, input_speed : int = 0, max_send_paquets : int = 0) -> None:
        Node.instance_counter += 1
        
        self.id : int = node_id                     # id du Nœud 
        self.name : str = name                      # nom du Nœud  
        self.type : str = node_type                 # le type du Nœud qui sera soit "Source", soit "Buffer", soit "Network"
        self.output_speed : int = output_speed      # vitesse de transmisison, si output_speed = 100 (Mb/s) alors si paquet est de 10Mb on aura 
        self.max_send_paquets = max_send_paquets    # marge maximum de paquet envoyer

        self.paquet_queue : list[Paquet] = []       # permet de stocker les paquets contenus dans chaque Nœud
        self.connections : int = 0                  # 
        self.last_update_time : float = 0           # permet de juger le temps avant d'update


    def create_paquet(self, data : str = None, size : int = None, tracking : bool = None) -> None:
        '''Créer un paquet et le stocke dans l'inventaire du Nœud'''
        paquet = Paquet(data, size, tracking)
        self.paquet_queue.append(paquet)


    def receve_paquet(self, paquet : Paquet) -> None:
        '''Stocke dans l'inventaire du Nœud le paquet'''
        self.paquet_queue.append(paquet)


    def send_paquet(self) -> None:
        '''Si l'inventaire du Nœud n'est pas vide : supprime et envoie un paquet présent'''
        if self.paquet_queue:
            return self.paquet_queue.pop(0)


    def show_paquet_queue(self) -> list[Paquet]:
        '''Affiche l'inventaire actuel du Nœud'''
        return self.paquet_queue


    def __repr__(self):
        '''Pour afficher proprement l'objet'''
        return f"'{self.type}:{self.name}'"


class Source(Node): 

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)        # héritage de la class Nœud
        Source.instance_counter += 1  

    def send_paquet(self) -> AttributeError:
        return AttributeError (" L'objet 'Source' n'a pas de méthode 'send_paquet' ")
    
    def receve_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( "'Source' object has no attribute 'receve_paquet'" )

    def get_paquet(self) :
        if self.paquet_queue :
            paq = self.paquet_queue[0]
            return paq



class Endpoint(Node):

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)       # héritage de la class Nœud
        
        Endpoint.instance_counter += 1


    def send_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( " l'objet 'Endpoint' n'a pas de méthode 'send_paquet'" )      # surcharge de la méthode


    def create_paquet(self, *args, **kwargs) -> Paquet:
        raise AttributeError( "'objet 'Endpoint' n'a pas de méthode 'create_paquet'" )      # surcharge de la méthode



class Buffer(Node):

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)       # héritage de la class Nœud

        Buffer.instance_counter += 1
        
        self.capacity = 10                          # capacité maximale du 'Buffer'
        self.number_element = 0                     # le nombre d'élément pour vérifier si ajout possible ou non
        self.paquet_queue = []                      # la liste qui représentera la file


    def receve_paquet(self, node) -> None:
        
        if self.number_element < self.capacity :    # ajout possible seulement si la capacité nous le permet
            if node.paquet_queue : 
                paquet = node.paquet_queue.pop(0)

                self.paquet_queue.append(paquet)
                self.number_element += 1
        
        else :
            del paquet                              # sinon on ignore le paquet


    def send_paquet(self) -> Paquet:                # si l'inventaire n'est pas vide on envoie
        if self.paquet_queue :  
            return self.paquet_queue.pop(0)