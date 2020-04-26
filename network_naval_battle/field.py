from ship import Ship
from gamer import Gamer
from random import randint


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

    def _set_around(self, x: int, y: int, new_type: str):
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

        if new_type == 'ship':
            self._field[x][y] = Ship(x, y)
        else:
            self._field[x][y] = self._cell_types[new_type]

    def get_cell(self, x: int, y: int):
        self._neg_check(x, y)

        return self._field[x][y]

    def random_ships_placed(self):
        ships_count = 6

        while ships_count:
            x = randint(0, 9)
            y = randint(0, 9)

            try:
                self.try_to_place_ship(x, y)
                ships_count -= 1
            except InaccessiblePlace:
                continue

    @staticmethod
    def _create_line(line: list):
        result = ''
        for cell in line:
            if cell:
                print(cell, end=' ')
                result += cell + ' '
            else:
                print('~', end=' ')
                result += '~ '

        return result

    def __str__(self):
        result = ''
        for line in self._field:
            result += self._create_line(line) + '\n'
            print()

        return result

    @classmethod
    def show_both_fields(cls):
        result = ''
        for i in range(10):
            for field in cls._fields:
                result += cls._create_line(field[i]) + ' ' * 6
                print(' ' * 6)

        return result


class NegativeParameter(Exception):
    pass


class InaccessiblePlace(Exception):
    pass
