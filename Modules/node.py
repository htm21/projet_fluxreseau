import string
import random as rd

from time import time
from math import log10
from random import uniform
from Modules.utils import *
from Modules.paquet import Paquet               # on importe la class Paquets dans le fichier pour pouvoir l'utiliser


class Node(object):                             # creation de la class mère "Node" 

    instance_counter : int = 0

    def __init__(self, node_id : int = None, name : str = None, node_type : str = None, paquet_size : int = None, lambda_const : int = None) -> None:
        Node.instance_counter += 1
        
        self.id : int = node_id                     
        self.name : str = name                      
        self.type : str = node_type                 # le type du Node : "Source" ou "Buffer" (décrit les class qui héritent de la class)     
        self.paquet_size = paquet_size              
        self.lambda_const = lambda_const

        self.paquet_queue : list[Paquet] = []       # initialisation de la FIFO
        self.connections : list[Node] = []         


    def generate_data(self):
        """ Fonction qui génère des chaînes aléatoires (qui seront interprétées comme des données) """
        return ''.join([rd.choice(string.ascii_letters + string.digits) for _ in range(5)])
    

    def create_paquet(self, data : str = None, size : int = None) -> None:
        """ Fonction qui créée un paquet et l'intègre dans la FIFO du Node """
        self.paquet_queue.append(Paquet(data, size))


    def receve_paquet(self, paquet : Paquet) -> None:
        """ Fonction qui ajoute les paquets reçu dans la FIFO du Node """
        self.paquet_queue.append(paquet)


    def show_paquet_queue(self) -> list[Paquet]:
        return self.paquet_queue


    def generate_wait_time(self) -> float:
        U = uniform(0.1, 1)
        product = -(1 / self.lambda_const) * log10(U)
        return product


    def calc_paquet_output(self) -> int:
        total_wait_time = 0
        paquet_output = 0
        while total_wait_time < 1:

            paquet_wait_time = self.generate_wait_time()
            if paquet_wait_time + total_wait_time > 1:
                break
            
            total_wait_time += paquet_wait_time
            paquet_output += 1
        return paquet_output


    def __repr__(self) -> str:
        ''' To properly display the object '''
        return f"'{self.type}:{self.name}'"



class Source(Node): 

    instance_counter : int = 0
    behaviour_types : list = [
        "Normal",
        "Buffered"
        ]


    def __init__(self, output : int, behaviour : str, capacity : int = None, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)        # héritage de la class Nœud
        Source.instance_counter += 1  


        self.output = output
        self.paquet_output = self.output // self.paquet_size  
        
        self.paquets_created = 0
        self.paquets_lost = 0 # total paquets lost during its existance

        self.behaviour : str = behaviour
        if self.behaviour == "Buffered":
            self.capacity = capacity

            self.paquet_loss = 0 # paquets lost during network update


    def create_paquets(self) -> None:
        """ Fonction qui s'occupe de crée des Paquets (en utilisant la fonction create_paquet et génère des donnée aléatoire à l'aide de generate_data() """
        for _ in range(self.paquet_output):
            self.create_paquet(data = self.generate_data(), size = self.paquet_size)


        self.paquets_created += self.paquet_output 
        if self.behaviour == "Buffered": 
            self.conform_paquet_queue()
        

    def conform_paquet_queue(self) -> None: 
        self.paquet_queue, rejected_paquets = self.paquet_queue[: self.capacity], self.paquet_queue[self.capacity :]
        self.paquet_loss = len(rejected_paquets)
        self.paquets_lost += self.paquet_loss


    def send_paquet(self) -> AttributeError:    
        return AttributeError (" L'objet 'Source' n'a pas de méthode 'send_paquet' ")       # Surchage des méthodes
    

    def receve_paquet(self, *args, **kwargs) -> AttributeError:
        raise AttributeError( "'Source' object has no attribute 'receve_paquet'" )          # ...


    def get_paquet(self) :
        if self.paquet_queue :
            paq = self.paquet_queue[0]
            return paq



class Buffer(Node):                                

    instance_counter : int = 0
    behaviour_types : list = [                     # les différents comportements possibles (Partie : Stratégie de Gestion)
        "Normal",
        "Biggest Queue",
        "Alternating",
        "Random"
        ]

    def __init__(self, behaviour : str = "Normal", capacity : int = 10, *args, **kwargs) -> None:   # Initialisation du Node "Buffer", qui a des attribut "behaviour" (comportement) et "capacity" (capacité) en plus
        Node.__init__(self, *args, **kwargs)       # héritage de la class Nœud
        Buffer.instance_counter += 1

        self.capacity : int = capacity                    # la capacité du Buffer
        self.number_element : int = 0                     

        self.behaviour : str = behaviour  
        self.behaviour_types : dict[str : function] = {             # dictionnaire permettant d'accèder à la fonction correspondante au comportement entré
        "Normal" : self.fifo,           
        "Biggest Queue" : self.biggest_queue,
        "Alternating" : self.alternating,
        "Random" : self.random_choice
        }

        self.paquet_transfer : int = 0                   
        self.paquets_transfered : int = 0                 # le nombre de paquets ayant atteint le réseau
        
        self.paquet_loss : int = 0
        self.paquets_lost : int = 0                       # le nombre de paquets ayant était perdu 

        self.mean_paquet_wait_time : int = 0


    def collect_paquets(self) -> None:
        """ Fonction qui permet de récuperer des paquets des Nodes connectés """
        extracted_paquets = self.behaviour_types[self.behaviour]()
        self.paquet_queue.extend(extracted_paquets)
        

        total_paquet_loss = 0
        for node in self.connections:
            if node.behaviour == "Normal" and not node.paquet_queue:
                total_paquet_loss += len(node.paquet_queue)
                node.paquet_queue.clear()
        self.paquet_loss = total_paquet_loss
        self.paquets_lost += self.paquet_loss


    def fifo(self) -> list[Paquet]:
        """ Fonction qui décrit le comportement initial du Buffer, une File d'Attente """    
        paquets = []
        exhausted_nodes = []
        
        max_index = len(self.connections)
        index = 0

        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):  
            node = self.connections[index]           
            if node not in exhausted_nodes:
                
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
                
                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                if not node.paquet_queue:
                    exhausted_nodes.append(node)

                paquets.extend(extracted_paquets)
                self.number_element += len(extracted_paquets)

            index = 0 if index == max_index else index + 1

        return paquets


    def biggest_queue(self) -> list[Paquet]:
        """ Fonction qui décrit le comportement additionnel du Buffer : le buffer choisit la "buffered" Source ayant la plus grande file (la plus remplie) """
        paquets = []
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            biggest_node_queue = self.connections[0]
            if node not in exhausted_nodes:
                
                for node in self.connections:
                    if len(node.paquet_queue) > len(biggest_node_queue.paquet_queue): 
                        biggest_node_queue = node

                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered" and node not in exhausted_nodes:
                    exhausted_nodes.append(node)
                    paquet_input = biggest_node_queue.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
                
                extracted_paquets, biggest_node_queue.paquet_queue = biggest_node_queue.paquet_queue[: paquet_input], biggest_node_queue.paquet_queue[paquet_input :]      
                
                if not node.paquet_queue:
                    exhausted_nodes.append(node)

                paquets.extend(extracted_paquets)         
                self.number_element += len(extracted_paquets)
        
        return paquets


    def alternating(self) -> list[Paquet]:
        """ Fonction qui décrit le comportement additionnel du Buffer : le buffer choisit de manière alternée les "buffered" Sources pour collecter les paquets """
        paquets = []    
        exhausted_nodes = []
        
        max_index = len(self.connections)
        index = 0
        
        lambda_tracker = dict()
        for node in self.connections:
            if node.behaviour == "Buffered":
                lambda_tracker[node] = float()

        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            node = self.connections[index]
            if node not in exhausted_nodes:
                
                if node.behaviour == "Buffered":
                    wait_time = node.generate_wait_time()
                    if lambda_tracker[node] + wait_time > 1:
                        exhausted_nodes.append(node)
                    else:
                        lambda_tracker[node] += wait_time
                        paquets.append(node.paquet_queue.pop(0))
                        self.number_element += 1     
                
                if node.behaviour == "Normal":
                    paquets.append(node.paquet_queue.pop(0))    
                    if not node.paquet_queue:
                        exhausted_nodes.append(node)
                    
                    self.number_element += 1     

            index = 0 if index == max_index else index + 1

        return paquets


    def random_choice(self) -> list[Paquet]:
        """ Fonction qui décrit le comportement additionnel du Buffer : le buffer choisit de manière aléatoire les "buffered" Sources qui lui sont connectées """
        paquets = []
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            node = rd.choice(self.connections)
            if node not in exhausted_nodes:
                
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input

                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                paquets.extend(extracted_paquets)  
                self.number_element += len(extracted_paquets)    

        return paquets


    def send_paquets(self):
        """ Fonction qui permet d'envoyer les paquets stockés au Réseau """

        paquet_output = self.calc_paquet_output()
        extracted_paquets, self.paquet_queue = self.paquet_queue[: paquet_output], self.paquet_queue[paquet_output :]
        
        if extracted_paquets:
            if self.mean_paquet_wait_time == 0:
                output_time = time()
                self.mean_paquet_wait_time = sum([output_time - paquet.creation_time for paquet in extracted_paquets]) / len(extracted_paquets)
            else:
                output_time = time()
                self.mean_paquet_wait_time = (sum([output_time - paquet.creation_time for paquet in extracted_paquets]) / len(extracted_paquets)) / 2

        self.paquet_transfer = len(extracted_paquets)   
        self.paquets_transfered += self.paquet_transfer 
        self.number_element -= len(extracted_paquets)   
    
