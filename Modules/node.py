import string
import random as rd

from time import time
from Modules.paquet import Paquet


class Node(object):

    instance_counter : int = 0

    def __init__(self, node_id : int = None, name : str = None, node_type : str = None, output_speed : int = None, paquet_size : int = None) -> None:
        Node.instance_counter += 1
        
        self.id : int = node_id                     # Canvas id du Nœud 
        self.name : str = name                      # nom du Nœud  
        self.type : str = node_type                 # le type du Nœud qui sera soit "Source", soit "Buffer", soit "Network"
        self.output_speed : int = output_speed      # vitesse de transmisison, si output_speed = 100 (Mb/s) alors si paquet est de 10Mb on aura 
        self.paquet_size = paquet_size

        self.paquet_queue : list[Paquet] = []       # permet de stocker les paquets contenus dans chaque Nœud
        self.connections : list[Node] = []


    def generate_data(self):
        return ''.join([rd.choice(string.ascii_letters + string.digits) for _ in range(5)]) 
    

    def create_paquet(self, data : str = None, size : int = None, tracking : bool = None) -> None:
        '''Créer un paquet et le stocke dans l'inventaire du Nœud'''
        self.paquet_queue.append(Paquet(data, size, tracking))


    def receve_paquet(self, paquet : Paquet) -> None:
        '''Stocke dans l'inventaire du Nœud le paquet'''
        self.paquet_queue.append(paquet)


    def show_paquet_queue(self) -> list[Paquet]:
        '''Affiche l'inventaire actuel du Nœud'''
        return self.paquet_queue


    def __repr__(self) -> str:
        '''Pour afficher proprement l'objet'''
        return f"'{self.type}:{self.name}'"



class Source(Node): 

    instance_counter : int = 0
    behaviour_types : dict = [
        "Normal",
        "Buffered"
        ]


    def __init__(self, behaviour : str, capacity : int = None, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)        # héritage de la class Nœud
        Source.instance_counter += 1  

        self.paquet_output = self.output_speed // self.paquet_size  
        
        self.paquets_created = 0

        self.behaviour : str = behaviour
        if self.behaviour == "Buffered":
            self.capacity = capacity
            self.paquets_lost = 0 # total paquets lost during its existance

            self.paquet_loss = 0 # paquets lost during network update


    def create_paquets(self) -> None:
        for _ in range(self.paquet_output):
            self.create_paquet(data = self.generate_data(), size = self.paquet_size, tracking = False)


        self.paquets_created += self.paquet_output 
        if self.behaviour == "Buffered": 
            self.conform_paquet_queue()
        

    def conform_paquet_queue(self) -> None: 
        self.paquet_queue, rejected_paquets = self.paquet_queue[: self.capacity], self.paquet_queue[self.capacity :]
        self.paquet_loss = len(rejected_paquets)
        self.paquets_lost += self.paquet_loss


    def send_paquet(self) -> AttributeError:
        return AttributeError (" L'objet 'Source' n'a pas de méthode 'send_paquet' ")
    

    def receve_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( "'Source' object has no attribute 'receve_paquet'" )


    def get_paquet(self) :
        if self.paquet_queue :
            paq = self.paquet_queue[0]
            return paq



class Buffer(Node):

    instance_counter : int = 0
    behaviour_types : list = [
        "Normal",
        "Biggest Queue",
        "Alternating",
        "Random"
        ]

    def __init__(self, behaviour : str = "Normal", capacity : int = 10, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)       # héritage de la class Nœud
        Buffer.instance_counter += 1

        self.capacity = capacity                    # capacité maximale du 'Buffer'
        self.number_element = 0                     # le nombre d'élément pour vérifier si ajout possible ou non
  
        self.behaviour = behaviour
        self.behaviour_types : dict = {
        "Normal" : self.fifo,
        "Biggest Queue" : self.biggest_queue,
        "Alternating" : self.alternating,
        "Random" : self.random_choice
        }

        self.paquet_output = self.output_speed  // self.paquet_size   

        self.paquet_transfer = 0
        self.paquets_transfered = 0

        self.paquet_loss = 0
        self.paquets_lost = 0

        self.mean_paquet_wait_time = 0


    def collect_paquets(self) -> None:
        total_paquets = 0
        for node in self.connections:
            total_paquets += len(node.paquet_queue)

        extracted_paquets = self.behaviour_types[self.behaviour](total_paquets)
        total_paquets -= len(extracted_paquets)
        self.paquet_queue.extend(extracted_paquets)
        
        if total_paquets:
            total_paquet_loss = 0
            for node in self.connections:
                total_paquet_loss += len(node.paquet_queue)
                node.paquet_queue.clear()
            self.paquet_loss = total_paquet_loss
            self.paquets_lost += self.paquet_loss


    def fifo(self, total_paquets : int) -> list[Paquet]:
        paquets = []
        while self.number_element != self.capacity and total_paquets != 0:
            for node in self.connections:
                if paquet_input := self.capacity - self.number_element:
                    print(paquet_input)
                    extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]


                    paquets.extend(extracted_paquets)
                    total_paquets -= len(extracted_paquets)
                    self.number_element += len(extracted_paquets)

        return paquets


    def biggest_queue(self, total_paquets : int) -> list[Paquet]:
        paquets = []
        while self.number_element != self.capacity and total_paquets != 0:
            paquet_input = self.capacity - self.number_element
            biggest_node_queue = self.connections[0]
            if len(self.connections) > 1:
                for node in self.connections:
                    if len(node.paquet_queue) > len(biggest_node_queue.paquet_queue): 
                        biggest_node_queue = node
            extracted_paquets, biggest_node_queue.paquet_queue = biggest_node_queue.paquet_queue[: paquet_input], biggest_node_queue.paquet_queue[paquet_input :]      


            paquets.extend(extracted_paquets)         
            total_paquets -= len(extracted_paquets)
            self.number_element += len(extracted_paquets)
        
        return paquets
        

    def alternating(self, total_paquets : int) -> list[Paquet]:
        paquets = []
        while self.number_element != self.capacity and total_paquets != 0:
            for node in self.connections:
                if node.paquet_queue:
                    paquets.append(node.paquet_queue.pop(0))
                    

                    self.number_element += 1
                    total_paquets -= 1
        
        return paquets


    def random_choice(self, total_paquets : int) -> list[Paquet]:
        paquets = []
        while self.number_element != self.capacity and total_paquets != 0:
            amount = self.capacity - self.number_element
            node = rd.choice(self.connections)
            extracted_paquets, node.paquet_queue = node.paquet_queue[: amount], node.paquet_queue[amount :]


            paquets.extend(extracted_paquets)  
            self.number_element += len(extracted_paquets)    
            total_paquets -= len(extracted_paquets)
        
        return paquets


    def send_paquets(self):
        extracted_paquets, self.paquet_queue = self.paquet_queue[: self.paquet_output], self.paquet_queue[self.paquet_output :]
        
        if extracted_paquets:
            if self.mean_paquet_wait_time == 0:
                self.mean_paquet_wait_time = sum([time() - paquet.creation_time for paquet in extracted_paquets]) / len(extracted_paquets)
            else:
                self.mean_paquet_wait_time = (self.mean_paquet_wait_time + (sum([time() - paquet.creation_time for paquet in extracted_paquets]) / len(extracted_paquets)) / 2)

        self.paquet_transfer = len(extracted_paquets)
        self.paquets_transfered += self.paquet_transfer
        self.number_element -= len(extracted_paquets)











# Decommissioned Node

class Endpoint(Node):

    instance_counter : int = 0

    def __init__(self, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)       # héritage de la class Nœud
        
        Endpoint.instance_counter += 1


    def send_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( " l'objet 'Endpoint' n'a pas de méthode 'send_paquet'" )      # surcharge de la méthode


    def create_paquet(self, *args, **kwargs) -> Paquet:
        raise AttributeError( "'objet 'Endpoint' n'a pas de méthode 'create_paquet'" )      # surcharge de la méthode


