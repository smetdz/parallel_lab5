from ship import Ship
from gamer import Gamer


class Field:
    _cell_types = {
        'water': '~',
        'destroyed': 'X',
        'fired': '*',
        'taken': '',
        'ship': Ship()
    }

    _fields = list()

    def __init__(self, gamer: Gamer):
        self._field = [[self._cell_types['water'] for _ in range(10)] for _ in range(10)]
        self._gamer = gamer
        self._fields.append(self)

    @staticmethod
    def _neg_check(x: int, y: int):
        if (x < 0) or (y < 0):
            raise NegativeParameter

    def _set_around(self, x: int, y: int, new_type: 'str'):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                try:
                    self._change_cell_type(i, y, new_type)
                except NegativeParameter:
                    continue

    def try_to_place_ship(self, x: int, y: int):
        if self._field[x][y] != self._cell_types['taken']:
            self._change_cell_type(x, y, 'ship')
            self._set_around(x, y, 'taken')
        else:
            raise InaccessiblePlace

    def _change_cell_type(self, x: int, y: int, new_type: str):
        self._neg_check(x, y)
        self._field[x][y] = self._cell_types[new_type]

    def get_cell(self, x: int, y: int):
        self._neg_check(x, y)
        return self._field[x][y]

    @staticmethod
    def _print_line(line: list):
        for cell in line:
            if cell:
                print(cell, end=' ')
            else:
                print('~')

    def __repr__(self):
        for line in self._field:
            self._print_line(line)
            print()

    @classmethod
    def show_both_fields(cls):
        for i in range(10):
            for field in cls._fields:
                cls._print_line(field[i])
                print('' * 6)


class NegativeParameter(Exception):
    pass


class InaccessiblePlace(Exception):
    pass
