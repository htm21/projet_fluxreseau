import string
import random as rd

from time import time
from math import log10
from random import uniform
from Modules.utils import *
from Modules.paquet import Paquet


class Node(object):
    '''
    La classe "Node" est la class Mère des class "Source" et "Buffer".
    Il regroupe les fonctions et les propriétés qui sont en commun avec les deux class enfants.
    '''

    instance_counter : int = 0

    def __init__(self, node_id : int = None, name : str = None, node_type : str = None, paquet_size : int = None, lambda_const : int = None) -> None:
        Node.instance_counter += 1
        
         # L’identifiant du nœud est utilisé pour accéder à l’objet tk.Canvas
        self.id : int = node_id                     
        

        self.name : str = name                      
        self.type : str = node_type                 # le type du Node : "Source" ou "Buffer" (décrit les class qui héritent de la class)     
        self.paquet_size : int = paquet_size              
        self.lambda_const : int = lambda_const

        # File d’attente où les paquets sont stockés
        self.paquet_queue : list[Paquet] = []

        # Liste de tous les nœuds auxquels le nœud est connecté 
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
        Calcule le temps d’attente avant qu’un "Paquet" soit envoyé avec la constante "Lambda" donnée par l’utilisateur. 
        '''
        # Float aléatoire entre 0,1 et 1
        U = uniform(0.1, 1)
        product = -(1 / self.lambda_const) * log10(U)
        return product


    def calc_paquet_output(self) -> int:
        '''
        Calcule le nombre de paquets pouvant être envoyés en seconde, en appliquant l'équivalent de la loi de Poisson
        "self.generate_wait_time"
        '''
        total_wait_time = 0
        paquet_output = 0

        # Addition des temps d’attente et compte les paquets jusqu’au temps de MAJ du Network (chaque cycle = 1 sec) 
        while total_wait_time < 1:
            paquet_wait_time = self.generate_wait_time()
            if paquet_wait_time + total_wait_time > 1:
                break     
            total_wait_time += paquet_wait_time
            paquet_output += 1
        
        # renvoie le nombre de paquets pouvant être envoyés
        return paquet_output


    def __repr__(self) -> str:
        '''' Pour afficher correctement l’objet '''
        return f"'{self.type}:{self.name}'"



class Source(Node): 
    '''
    Class enfant de la class "Node".
    Un type "Source" de type "Node" est capable de générer des données de paquet.
    S’il est créé avec un Buffer (partie 2), ne pourra transmettre que des paquets selon la loi de Poissons
    '''
    instance_counter : int = 0
    behaviour_types : list = [
        "Normal",
        "Buffered"
        ]


    def __init__(self, output : int, behaviour : str, capacity : int = None, *args, **kwargs) -> None:
        Node.__init__(self, *args, **kwargs)        # héritage de la class Nœud
        Source.instance_counter += 1  

        # ATTENTION : LA SORTIE N’EST PAS LA VITESSE À LAQUELLE LES PAQUETS SONT TRANSMIS AUX TAMPONS
        self.output = output
        
        # Sortie du paquet calculée en fonction de la taille paquet du Réseaux choisie
        self.paquet_output = self.output // self.paquet_size  
        
        # Suit les paquets qui sont créés et perdus pendant leurs existances
        self.paquets_created = 0
        self.paquets_lost = 0

        self.behaviour : str = behaviour
        if self.behaviour == "Buffered":
            self.capacity = capacity
            # Suit les paquets perdus en raison de la file d’attente du Buffer de la Source
            self.paquet_loss = 0


    def create_paquets(self) -> None:
        '''
        Fonction qui s'occupe de crée des Paquets (en utilisant la fonction create_paquet et génère des donnée aléatoire à l'aide de generate_data() 
        '''
        for _ in range(self.paquet_output):
            self.create_paquet(data = self.generate_data(), size = self.paquet_size)


        self.paquets_created += self.paquet_output 
        if self.behaviour == "Buffered": 
            self.conform_paquet_queue()
        

    def conform_paquet_queue(self) -> None:
        '''
        Si le nœud "Source" est mis en mémoire tampon, la file d’attente du paquet sera conforme à la capacité du tampon, le reste étant supprimé
        et compté comme une perte. 
        '''
        self.paquet_queue, rejected_paquets = self.paquet_queue[: self.capacity], self.paquet_queue[self.capacity :]
        self.paquet_loss = len(rejected_paquets)
        self.paquets_lost += self.paquet_loss



class Buffer(Node):                                
    '''
    Class enfant de la class "Node".
    Un "Buffer" type "Node" est capable de prendre des paquets de "Source" type "Nodes" et de les transmettre à 
    réseau (retrait de la file d’attente du Buffer) selon la loi Poissons.
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

        # Capacité du Buffer et son nombre actuel d'élément
        self.capacity : int = capacity
        self.number_element : int = 0                     

        # Comportement du Buffer et ses fonctions correspondantes
        self.behaviour : str = behaviour  
        self.behaviour_types : dict[str : function] = {
        "Normal" : self.fifo,           
        "Biggest Queue" : self.biggest_queue,
        "Alternating" : self.alternating,
        "Random" : self.random_choice
        }

        # Suivi les paquets envoyés au total et pendant le cycle de MAJ
        self.paquet_transfer : int = 0                   
        self.paquets_transfered : int = 0              

        # Suivi des paquets lsot au total et pendant le cycle de MAJ
        self.paquet_loss : int = 0
        self.paquets_lost : int = 0

        # Temps moyen d'attente des paquets
        self.mean_paquet_wait_time : int = 0


    def collect_paquets(self) -> None:
        '''
        Fonction qui permet de récuperer des paquets des Nodes connectés
        '''
        
        # Exécute la fonction liée au comportement des Buffer
        extracted_paquets = self.behaviour_types[self.behaviour]()
        
        # Ajoute les paquets que l'on a récupéré à la file 
        self.paquet_queue.extend(extracted_paquets)
        
        # Compter la perte totale de paquets des sources normales car elles n’ont pas de Buffer pour stocker les paquets non transférés
        # & les supprimés de la file d’attente des paquets sources
        total_paquet_loss = 0
        for node in self.connections:
            if node.behaviour == "Normal" and not node.paquet_queue:
                total_paquet_loss += len(node.paquet_queue)
                node.paquet_queue.clear()
        self.paquet_loss = total_paquet_loss
        self.paquets_lost += self.paquet_loss


    def fifo(self) -> list[Paquet]:
        '''
        La fonction fifo passera par tous les nœuds et prendra autant de paquets qu’elle peut dans en prennant le temps de connection comme ordre respectif
        '''       
        # Les paquets collectés forment les sources
        paquets = []
        
        # Les sources qui ne peuvent plus donner de paquets sont "bannies" et stockées ici
        # Si une source n’a plus de paquets ou ne peut plus en donner puisque son buffer suit la loi de Poisson
        exhausted_nodes = []
        
        # Utilisé pour parcourir les nœuds dans la liste self.connections (FIFO)
        max_index = len(self.connections) - 1
        index = 0
    
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):  
            node = self.connections[index]           
            if node not in exhausted_nodes:
                
                # quantité de paquets que nous pouvons extraire du nœud source s’il est mis en mémoire si "buffered" ou non
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
                
                # Extraction de paquets par coupes et "unpacking" de tuple 
                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                # si la source n’a plus de nœuds à donner, elle est marqué comme "épuisée"/exhausted
                if not node.paquet_queue:
                    exhausted_nodes.append(node)

                # mettre à jour la file d’attente du Buffer et MAJ de la capacité restante
                paquets.extend(extracted_paquets)
                self.number_element += len(extracted_paquets)
            
            # index du nœud suivant dans la liste else "loop back"
            index = 0 if index == max_index else index + 1

        # retourne les paquets extraits (liste)
        return paquets


    def biggest_queue(self) -> list[Paquet]:
        '''
        La fonction biggest_queue parcourt tous les nœuds et prend autant de paquets qu’elle peut mais donne 
        la priorité à la source qui à la plus grande file d’attente de paquets.
        '''
        # Paquets qui sont récupérés des sources
        paquets = []

        # Les sources qui ne peuvent plus donner de paquets sont "bannies" et stockées ici
        # Si une source n’a plus de paquets ou ne peut plus en donner puisque son buffer suit la loi de Poisson
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            # trouve la source avec la plus grande file de paquets
            biggest_node_queue = self.connections[0]            
            for node in self.connections:
                if len(node.paquet_queue) > len(biggest_node_queue.paquet_queue) and node not in exhausted_nodes: 
                    biggest_node_queue = node

            # quantité de paquets que nous pouvons extraire du nœud Source s’il est mis en mémoire s'il est "bufferisé" ou pas
            max_paquet_input = self.capacity - self.number_element
            paquet_input = max_paquet_input             
            if biggest_node_queue.behaviour == "Buffered":
                exhausted_nodes.append(node)
                paquet_input = biggest_node_queue.calc_paquet_output()
                paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input
            
            # Extraction de paquets par coupes et "unpacking" de tuple 
            extracted_paquets, biggest_node_queue.paquet_queue = biggest_node_queue.paquet_queue[: paquet_input], biggest_node_queue.paquet_queue[paquet_input :]      
            
            # si la source n’a plus de nœuds à donner, elle est marqué comme "épuisée"/exhausted
            if not node.paquet_queue:
                exhausted_nodes.append(node)

            # MAJ de la file d’attente du Buffer et de sa capacité 
            paquets.extend(extracted_paquets)         
            self.number_element += len(extracted_paquets)
        
        # retourne les paquets extraits (liste)
        return paquets


    def alternating(self) -> list[Paquet]:
        '''
        La fonction alternative extrait les paquets des nœuds Source un par un tout en alternant
        entre les nœuds connectés dans l’ordre FIFO. 
        '''
        # Les paquets collectés forment les sources
        paquets = []    
        
        # Les sources qui ne peuvent plus donner de paquets sont "bannies" et stockées ici
        # Si une source n’a plus de paquets ou ne peut plus en donner puisque son buffer suit la loi de Poisson
        exhausted_nodes = []
        
        # Utilisé pour parcourir les nœuds dans la liste self.connections (FIFO)
        max_index = len(self.connections) - 1
        index = 0
        
        # Tacks pour toutes les sources "bufferisés", le temps d’attente total de chaque paquet extrait
        # Utilisé pour à 1 seconde
        lambda_tracker = dict()
        for node in self.connections:
            if node.behaviour == "Buffered":
                lambda_tracker[node] = 0

        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            node = self.connections[index]
            if node not in exhausted_nodes:
                if node.paquet_queue:
                    
                    if node.behaviour == "Normal":
                        # Extrait le paquet de la file
                        paquets.append(node.paquet_queue.pop(0))    
                        # MAJ la capacité actuelle
                        self.number_element += 1 
                    
                    elif node.behaviour == "Buffered":
                        # Vérifie si le temps d’attente du paquet + le temps d’attente total de tous les paquets 
                        # actuellement ajoutés  est suppérieur à 1
                        wait_time = node.generate_wait_time()
                        if lambda_tracker[node] + wait_time > 1:
                            exhausted_nodes.append(node)
                        else:
                            # si le temps d’attente total du paquet est toujours < 1 seconde, le paquet est extrait
                            lambda_tracker[node] += wait_time
                            paquets.append(node.paquet_queue.pop(0))
                            self.number_element += 1         
                else:
                    exhausted_nodes.append(node)
            # index du nœud suivant dans la liste else "loop back"
            index = 0 if index == max_index else index + 1

        # retourne les paquets extraits (liste)
        return paquets


    def random_choice(self) -> list[Paquet]:
        '''
        La fonction random_choice choisira un nœud source aléatoire pour en prendre autant 
        paquets qu’il peut.
        '''
        # Les paquets collectés forment les sources
        paquets = []
        
        # Les sources qui ne peuvent plus donner de paquets sont "bannies" et stockées ici
        # Si une source n’a plus de paquets ou ne peut plus en donner puisque son buffer suit la loi de Poisson
        exhausted_nodes = []
        
        while self.number_element != self.capacity and len(exhausted_nodes) != len(self.connections):
            # Prend un nœud aléatoire dans self.connections
            node = rd.choice(self.connections)
            if node not in exhausted_nodes: 

                # quantité de paquets que nous pouvons extraire du nœud source s’il est "bufferisé" ou non   
                max_paquet_input = self.capacity - self.number_element
                paquet_input = max_paquet_input             
                if node.behaviour == "Buffered":
                    exhausted_nodes.append(node)
                    paquet_input = node.calc_paquet_output()
                    paquet_input = max_paquet_input if paquet_input > max_paquet_input else paquet_input

                # Extraction de paquets par coupes et "unpacking" de tuple 
                extracted_paquets, node.paquet_queue = node.paquet_queue[: paquet_input], node.paquet_queue[paquet_input :]

                # MAJ des données du Buffer
                paquets.extend(extracted_paquets)  
                self.number_element += len(extracted_paquets)    

        # return the paquets extracted (list)
        return paquets


    def send_paquets(self):
        '''
        Cette fonction représente le nœud Buffer "envoyant" les paquets dans la
        file d’attente de paquet sur le réseau. 
        Le Buffer va effectivement extraire les paquets de sa file d’attente de paquets selon la loi Poissons, 
        les additionner, calculer le temps d’attente moyen des paquets et les supprimés.  
        '''

        # extraire les paquets de sa file d’attente de paquets suivant la loi Poissons
        # Extraction de paquets par coupes et déballage de tuple 
        paquet_output = self.calc_paquet_output()
        extracted_paquets, self.paquet_queue = self.paquet_queue[: paquet_output], self.paquet_queue[paquet_output :]
        
        # MAJ des chiffres de "tracking" 
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