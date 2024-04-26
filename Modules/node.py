import string
import random as rd

from time import time
from math import log10
from random import uniform
from Modules.utils import *
from Modules.paquet import Paquet


class Node(object):
    '''
    The "Node" class is a Parent class to the "Source" and "Buffer" classes.
    It groups the functions and properties that are in common with both child classes.
    '''

    instance_counter : int = 0

    def __init__(self, node_id : int = None, name : str = None, node_type : str = None, paquet_size : int = None, lambda_const : int = None) -> None:
        Node.instance_counter += 1
        
        # The node id is used to acces the tk.Canvas object
        self.id : int = node_id                     
        

        self.name : str = name                      
        self.type : str = node_type                 # le type du Node : "Source" ou "Buffer" (décrit les class qui héritent de la class)     
        self.paquet_size : int = paquet_size              
        self.lambda_const : int = lambda_const

        # Queue where paquets are stored
        self.paquet_queue : list[Paquet] = []

        # List of all nodes that the node is connected to. 
        self.connections : list[Node] = []         


    def generate_data(self):
        """ Fonction qui génère des chaînes aléatoires (qui seront interprétées comme des données) """
        return ''.join([rd.choice(string.ascii_letters + string.digits) for _ in range(5)])
    

    def create_paquet(self, data : str = None, size : int = None) -> None:
        """ Fonction qui créée un paquet et l'intègre dans la queue du Node """
        self.paquet_queue.append(Paquet(data, size))


    def receve_paquet(self, paquet : Paquet) -> None:
        """ Fonction qui ajoute les paquets reçu dans la queue du Node """
        self.paquet_queue.append(paquet)


    def generate_wait_time(self) -> float:
        '''
        Calculates the wait time before a "Paquet" is sent with the user given "Lambda" constant. 
        '''
        # Random float between 0.1 and 1
        U = uniform(0.1, 1)
        product = -(1 / self.lambda_const) * log10(U)
        return product


    def calc_paquet_output(self) -> int:
        '''
        Calculates the amount of paquets that able to be sent in second, applying the Poisson probability function
        "self.generate_wait_time"
        '''
        total_wait_time = 0
        paquet_output = 0

        # Adding up wait times and counting paquets up to the update time of the network (every cycle = 1 sec) 
        while total_wait_time < 1:
            paquet_wait_time = self.generate_wait_time()
            if paquet_wait_time + total_wait_time > 1:
                break     
            total_wait_time += paquet_wait_time
            paquet_output += 1
        
        # returns the amount of paquets that can be sent
        return paquet_output


    def __repr__(self) -> str:
        ''' To properly display the object '''
        return f"'{self.type}:{self.name}'"



class Source(Node): 
    '''
    Child class of the "Node" class.
    A "Source" type "Node" is able to generate paquet data.
    If created with a buffer, will only be able to transmit paquets according to Poissons law
    '''
    instance_counter : int = 0
    behaviour_types : list = [
        "Normal",
        "Buffered"
        ]


    def __init__(self, output : int, behaviour : str, capacity : int = None, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)        # héritage de la class Nœud
        Source.instance_counter += 1  

        # THE OUTPUT IS NOT THE SPEED AT WHICH PAQUETS ARE TRANSMITTED TO BUFFERS
        self.output = output
        
        # Paquet output calculated given the "Networks" pauquet size
        self.paquet_output = self.output // self.paquet_size  
        
        # Tracks pauquets that are created and lost during its existance
        self.paquets_created = 0
        self.paquets_lost = 0

        self.behaviour : str = behaviour
        if self.behaviour == "Buffered":
            self.capacity = capacity
            # Tracks pauquets that are lost due to buffer queue
            self.paquet_loss = 0


    def create_paquets(self) -> None:
        """ Fonction qui s'occupe de crée des Paquets (en utilisant la fonction create_paquet et génère des donnée aléatoire à l'aide de generate_data() """
        for _ in range(self.paquet_output):
            self.create_paquet(data = self.generate_data(), size = self.paquet_size)


        self.paquets_created += self.paquet_output 
        if self.behaviour == "Buffered": 
            self.conform_paquet_queue()
        

    def conform_paquet_queue(self) -> None:
        '''
        If the "Source" node is buffered the paquet queue will be conformed to the buffer capacity, with the rest being removed
        and counted as loss. 
        '''
        self.paquet_queue, rejected_paquets = self.paquet_queue[: self.capacity], self.paquet_queue[self.capacity :]
        self.paquet_loss = len(rejected_paquets)
        self.paquets_lost += self.paquet_loss



class Buffer(Node):                                
    '''
    Child class of the "Node" class.
    A "Buffer" type "Node" is able to take paquets from "Source" type "Nodes" and transmit them to 
    network (removing from buffer queue) according to Poissons law.
    '''
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

        # Buffer capacity and its current queue size
        self.capacity : int = capacity
        self.number_element : int = 0                     

        # Buffer behaviour and its corresponding functions
        self.behaviour : str = behaviour  
        self.behaviour_types : dict[str : function] = {
        "Normal" : self.fifo,           
        "Biggest Queue" : self.biggest_queue,
        "Alternating" : self.alternating,
        "Random" : self.random_choice
        }

        # Tracking for paquets sent in total and during the update cycle
        self.paquet_transfer : int = 0                   
        self.paquets_transfered : int = 0              

        # Tracking for paquets lsot in total and during update cycle
        self.paquet_loss : int = 0
        self.paquets_lost : int = 0

        # Avrage paquet wait time
        self.mean_paquet_wait_time : int = 0


    def collect_paquets(self) -> None:
        """ Fonction qui permet de récuperer des paquets des Nodes connectés """
        
        # Executes the function tied to the buffers behaviour
        extracted_paquets = self.behaviour_types[self.behaviour]()
        # Add collected paquets to queue
        self.paquet_queue.extend(extracted_paquets)
        
        # Counting total Paquet loss of Normal Sources as they have no buffers to store any non transfered paquets
        # & deleting them from the sources paquet queue
        total_paquet_loss = 0
        for node in self.connections:
            if node.behaviour == "Normal" and not node.paquet_queue:
                total_paquet_loss += len(node.paquet_queue)
                node.paquet_queue.clear()
        self.paquet_loss = total_paquet_loss
        self.paquets_lost += self.paquet_loss


    def fifo(self) -> list[Paquet]:
        '''
        The fifo function will go through all nodes and take as many paquets that it can in the order of time connected.
        '''    
        # Paquets collected form the sources
        paquets = []
        
        # Sources that can't give anymore paquets are "banned" and stored in here
        # If a source has no more paquets or can't give any more paquets since its buffer follows the Poisson law
        exhausted_nodes = []
        
        # Used to go through the nodes within the self.connections list (FIFO)
        max_index = len(self.connections)
        index = 0
    
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):  
            node = self.connections[index]           
            if node not in exhausted_nodes:
                
                # amount of paquets we can extract from the source node if its buffered or not
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
                
                # Paquet extraction through slices and tuple unpacking 
                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                # if the source has no more nodes to give it is marked as "exhausted"
                if not node.paquet_queue:
                    exhausted_nodes.append(node)

                # update buffer queue and remaning capacity
                paquets.extend(extracted_paquets)
                self.number_element += len(extracted_paquets)
            
            # next node index in the list else loop back
            index = 0 if index == max_index else index + 1

        # return the paquets extracted (list)
        return paquets


    def biggest_queue(self) -> list[Paquet]:
        '''
        The biggest_queue function will go through all nodes and take as many paquets that it can but gives 
        priority to the source that has with the biggest paquet queue.
        '''
        # Paquets collected form the sources
        paquets = []

        # Sources that can't give anymore paquets are "banned" and stored in here
        # If a source has no more paquets or can't give any more paquets since its buffer follows the Poisson law
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            # finds source with the biggest paquet queue
            biggest_node_queue = self.connections[0]            
            for node in self.connections:
                if len(node.paquet_queue) > len(biggest_node_queue.paquet_queue) and node not in exhausted_nodes: 
                    biggest_node_queue = node

            # amount of paquets we can extract from the source node if its buffered or not
            max_paquet_input = self.capacity - self.number_element
            paquet_input = max_paquet_input             
            if biggest_node_queue.behaviour == "Buffered":
                exhausted_nodes.append(node)
                paquet_input = biggest_node_queue.calc_paquet_output()
                paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
            
            # Paquet extraction through slices and tuple unpacking 
            extracted_paquets, biggest_node_queue.paquet_queue = biggest_node_queue.paquet_queue[: paquet_input], biggest_node_queue.paquet_queue[paquet_input :]      
            
            # if the source has no more nodes to give it is marked as "exhausted"
            if not node.paquet_queue:
                exhausted_nodes.append(node)

            # update buffer queue and remaning capacity
            paquets.extend(extracted_paquets)         
            self.number_element += len(extracted_paquets)
        
        # return the paquets extracted (list)
        return paquets


    def alternating(self) -> list[Paquet]:
        '''
        The alternating function will extract paquets from source nodes one by one while alternating
        between the connected nodes in FIFO order. 
        '''
        # Paquets collected form the sources
        paquets = []    
        
        # Sources that can't give anymore paquets are "banned" and stored in here
        # If a source has no more paquets or can't give any more paquets since its buffer follows the Poisson law
        exhausted_nodes = []
        
        # Used to go through the nodes within the self.connections list (FIFO)
        max_index = len(self.connections)
        index = 0
        
        # Tacks for all buffered sources, the total wait time of each paquet extracted
        # Used to limit upto 1 second
        lambda_tracker = dict()
        for node in self.connections:
            if node.behaviour == "Buffered":
                lambda_tracker[node] = 0

        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            node = self.connections[index]
            if node not in exhausted_nodes:
                if not node.paquet_queue:
                    exhausted_nodes.append(node)
                
                elif node.behaviour == "Buffered":
                    # Checks if wait time of paquet + total wait time of all paquets 
                    # currently extraceted > 1
                    wait_time = node.generate_wait_time()
                    if lambda_tracker[node] + wait_time > 1:
                        exhausted_nodes.append(node)
                    else:
                        # if total paquet wait time is still < 1 second then the paquet is extracted
                        lambda_tracker[node] += wait_time
                        paquets.append(node.paquet_queue.pop(0))
                        self.number_element += 1     
                
                elif node.behaviour == "Normal":
                    # Takes paquet out of paquet queue
                    paquets.append(node.paquet_queue.pop(0))    
                    if not node.paquet_queue:
                        exhausted_nodes.append(node)
                    
                    # update remaning capacity
                    self.number_element += 1     

            # next node index in the list else loop back
            index = 0 if index == max_index else index + 1

        # return the paquets extracted (list)
        return paquets


    def random_choice(self) -> list[Paquet]:
        '''
        The random_choice function will pick a random source node to take as many 
        paquets that it can.
        '''
        # Paquets collected form the sources
        paquets = []
        
        # Sources that can't give anymore paquets are "banned" and stored in here
        # If a source has no more paquets or can't give any more paquets since its buffer follows the Poisson law
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            # Takes a random node from "self.connections"
            node = rd.choice(self.connections)
            if node not in exhausted_nodes: 

                # amount of paquets we can extract from the source node if its buffered or not   
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input

                # Paquet extraction through slices and tuple unpacking 
                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                # update buffer queue and remaning capacity
                paquets.extend(extracted_paquets)  
                self.number_element += len(extracted_paquets)    

        # return the paquets extracted (list)
        return paquets


    def send_paquets(self):
        '''
        This function represents the buffer node "sending" the paquets in the 
        paquet queue onto the network. 
        The Buffer will actualy extract the paquets form its paquet queue following Poissons law, 
        tally them up, calculate avrage paquet wait time and then delete them.  
        '''

        # extracting the paquets form its paquet queue following Poissons law
        # Paquet extraction through slices and tuple unpacking 
        paquet_output = self.calc_paquet_output()
        extracted_paquets, self.paquet_queue = self.paquet_queue[: paquet_output], self.paquet_queue[paquet_output :]
        
        # update paqute tracking values 
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
    
