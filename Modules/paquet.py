


class Paquet(object):
    def __init__(self, endpoit, data, size = None) -> None:
        self.endpoint = endpoit # Name of Endpoint Node
        self.data = data # can be anything (Symbols, Numbers etc...)
        self.size = size # in bytes
