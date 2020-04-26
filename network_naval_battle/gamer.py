class Gamer:
    def __init__(self, socket, field, name):
        self.socket = socket
        self.field = field
        self.name = name

    @property
    def get_socket(self):
        return self.socket

    @property
    def get_field(self):
        return self.field

    @property
    def get_name(self):
        return self.name
