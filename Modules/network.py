from Modules.node import Node, Source, Buffer, Endpoint

class Network(object):

    instance_counter = 0

    def __init__(self, name : str = None) -> None:
        Network.instance_counter += 1

        self.name = name if name else f"Network-{Network.instance_counter}"

        self.nodes : dict[str : Node] = {} # Sources, Endpoints or Buffers in the network
        self.links : set[tuple] = {} # Links between nodes
        self.NODE_TYPES = {
            "Source" : Source,
            "Endpoint" : Endpoint,
            "Buffer" : Buffer
            }



    def add_node(self, node_type = "Source", name = None, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network object by adding it to the "self.nodes" dictionary.
        If no node type is given it defaults to a "Source" type Node
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Source-1  
        
        '''

        class_type = self.NODE_TYPES.get(node_type)
        
        if not class_type:
            raise KeyError(f" '{node_type}' is not a valid node type")
        else:
            if not name:
                name = f"{node_type}-{self.NODE_TYPES.get(node_type).instance_counter}"
            
        self.nodes[name] = self.NODE_TYPES.get(node_type)(name = name, node_type = node_type, *args, **kwargs)
        # Use Node name to acces the object in the dict of nodes


    def del_node(self, node : str) -> None:
        '''
        Deletes a Node from the network by deleting the node from the "self.nodes" dictionary 
        and deleting all existing links to the deleted node from the "self.links" set.
        '''

        del self.nodes[node] 
        
        for connection in self.links:
            if node in connection:
                del connection


    def create_link(self, node_1, node_2, bandwidth) -> None:
        pass

    
    def info(self):
        '''
        Outputs a simple overview of the networks state
        '''

        print(f"\nNetwork : {self.name}")
        print(f"Nodes : {len(self.nodes)}")
        print(f"    Sources : {Source._instance_counter}")
        print(f"    Endpoints : {Endpoint._instance_counter}")
        print(f"    Buffers : {0}") # Buffer._instance_counter (TBD)
        print(f"Connections : {len(self.links)}\n")
