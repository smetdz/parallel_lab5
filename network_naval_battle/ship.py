class Ship:
    def __init__(self, x: int = None, y: int = None):
        self._is_alive = True
        self._x = x
        self._y = y

    @property
    def is_alive(self):
        return self._is_alive

    def kill(self):
        self._is_alive = False

    def __str__(self):
        if self.is_alive:
            return '[ ]'
        return '[x]'
