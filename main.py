import time
import Modules.utils
from Modules.network import Network
from Modules.paquet import Paquet
from Modules.node import Node, Source, Buffer, Endpoint


def main() -> None:

    network = Network()

    while network:
        if network.nodes:
            "taking care of node interactions"



if __name__ == "__main__":
    print("\033c") # Clear Terminal Start
    main()
    print("\033c") # Clear Terminal End
