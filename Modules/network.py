from Modules.node import Node, Source, Buffer, Endpoint

class Network(object):

    def __init__(self, name : str = None) -> None:

        self.name = name if name else f"Network"

        self.nodes : dict[str : Node] = {} # Sources, Endpoints or Buffers in the network
        self.links : set[tuple[str, str]] = set() # Links between nodes
        self.NODE_TYPES = {
            "Source" : Source,
            "Endpoint" : Endpoint,
            "Buffer" : Buffer,
            "Node" : Node
            }


    def add_node(self, node_type = "Node", name = None, *args, **kwargs) -> None:
        '''
        Creates a node and adds it onto the network object by adding it to the "self.nodes" dictionary.
        If no node type is given it defaults to a "Node" type Node (Not defined node)
        If no name is given to the node it will be automaticaly given one using this formatting: "NODE_TYPE-NODE_TYPE.instance_counter" -> Node-1  
        '''

        class_type = self.NODE_TYPES.get(node_type)
        
        if not class_type:
            raise KeyError(f" '{node_type}' is not a valid node type")
        
        if not name:
            name = f"{node_type}-{self.NODE_TYPES.get(node_type).instance_counter}"
            
        self.nodes[name] = self.NODE_TYPES.get(node_type)(name = name, node_type = node_type, *args, **kwargs)
        # Use Node name to acces the node object in the dict of nodes


    def del_node(self, node : str) -> None:
        '''
        Deletes a Node from the network by deleting the node from the "self.nodes" dictionary 
        and deleting all existing links to the deleted node from the "self.links" set.
        '''

        del self.nodes[node] 
        
        for connection in self.links:
            if node in connection:
                del connection


    def create_link(self, node_1 : str, node_2 : str) -> None:
        '''
        Creates a link between two nodes if it satisfies the linking requirements
        Adds a tuple(node_name, node_name) to the 'self.links' set
        '''
        
        if (node_1, node_2) in self.links:
            return
        
        elif self.nodes[node_1].type == "Node" or self.nodes[node_2].type == "Node":
            
            raise TypeError(f" Type 'Node' must be defined before linking")

        elif self.nodes[node_1].type == "Source" and self.nodes[node_2].type == "Source":

            raise TypeError(f" Type 'Source' cannot be link to a 'Source' node")

        else:    
            self.links.add((node_1, node_2))

    
    def info(self):
        '''
        Outputs a simple overview of the networks state
        '''
       
        print()
        

        # f"{self.name}\nNodes : {len(self.nodes)}     Sources : {Source.instance_counter}     Endpoints : {Endpoint.instance_counter}     Buffers : {Buffer.instance_counter}\nConnections : {len(self.links)}"

        print(f"{self.name}")
        print(f"\nNodes : {len(self.nodes)}")
        print(f"    Sources : {Source.instance_counter}")
        print(f"    Endpoints : {Endpoint.instance_counter}")
        print(f"    Buffers : {Buffer.instance_counter}")
        print(f"\nConnections : {len(self.links)}")
        for connection in self.links:
            print(f"    {connection[0]} | {connection[1]}")
        
        print()