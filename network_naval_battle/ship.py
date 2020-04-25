class Ship:
    def __init__(self):
        self.__is_alive = True

    @property
    def is_alive(self):
        return self.__is_alive

    def kill(self):
        self.__is_alive = False
