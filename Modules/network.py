from Modules.node import Source, Buffer, Endpoint

class Network(object):

    _instance_counter = 0

    def __init__(self, name : str = None) -> None:
        Network._instance_counter += 1

        self.name = name if name else f"Network-{Network._instance_counter}"

        self.nodes : dict[dict] = {} # Sources, Endpoints or Buffers in the network
        self.links : set[tuple] = {} # Links between nodes
        self.NODE_TYPES = {
            "Source" : Source,
            "Endpoint" : Endpoint,
            "Buffer" : Buffer
            }


    def add_node(self, node_type = None, name = None, *args, **kwargs) -> None:
        class_type = self.NODE_TYPES.get(node_type)
        
        if not class_type:
            raise KeyError(f" '{node_type}' is not a valid node type")
        
        else:
            if not name:
                name = f"{node_type}-{self.NODE_TYPES.get(node_type)._instance_counter}"
            
            self.nodes[name] = self.NODE_TYPES.get(node_type)(name = name, node_type = node_type, *args, **kwargs)
            # Use Node name to acces the object in the dict of nodes


    def del_node(self, name) -> None:
        # removes a Source node or a Endpoit node to the network
        pass


    def create_link(self, node_name_1, node_name_2, bandwidth) -> None:
        # creates a link between two nodes
        pass


    def info(self):
        print(f"\nNetwork : {self.name}")
        print(f"Nodes : {len(self.nodes)}")
        print(f"    Sources : {Source._instance_counter}")
        print(f"    Endpoints : {Endpoint._instance_counter}")
        print(f"    Buffers : {0}") # Buffer._instance_counter (TBD)
        print(f"Connections : {len(self.links)}\n")
