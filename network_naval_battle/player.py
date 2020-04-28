class Player:
    def __init__(self, socket, addr, field, name):
        self._socket = socket
        self._addr = addr
        self.field = field
        self._name = name
        self._ships_count = 6

    @property
    def socket(self):
        return self._socket

    @property
    def get_field(self):
        return self.field

    @property
    def name(self):
        return self._name

    @property
    def is_lose(self):
        return not bool(self._ships_count)

    @property
    def ships_count(self):
        return self._ships_count

    @ships_count.setter
    def ships_count(self, count):
        self._ships_count = count
