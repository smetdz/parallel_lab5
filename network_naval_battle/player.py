class Player:
    def __init__(self, socket, addr, field, name):
        self.socket = socket
        self.addr = addr
        self.field = field
        self.name = name
        self.ships_count = 6

    @property
    def get_socket(self):
        return self.socket

    @property
    def get_field(self):
        return self.field

    @property
    def get_name(self):
        return self.name

    @property
    def is_lose(self):
        return not bool(self.ships_count)
