import time
import Modules.utils
from Modules.network import Network
from Modules.paquet import Paquet
from Modules.node import Node, Source, Buffer, Endpoint




resau = Network()

resau.add_node("Source")
# resau.add_node("Buffer")
resau.add_node("Endpoint")

resau.info()
