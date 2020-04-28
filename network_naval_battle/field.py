from ship import Ship
from random import randint


class Field:
    _cell_types = {
        'water': ' ~ ',
        'fired': ' * ',
        'taken': '',
        'ship': Ship()
    }

    _fields = list()
    _field_size = 6
    _ships_count = 6

    def __init__(self):
        self._field = [[self._cell_types['water'] for _ in range(self._field_size)] for _ in range(self._field_size)]
        self._fields.append(self)

    @property
    def field_size(self):
        return self._field_size

    @property
    def ships_count(self):
        return self._ships_count

    def _check(self, x: int, y: int):
        if x not in range(self._field_size) or y not in range(self._field_size):
            raise BadParameter

    def set_around(self, x: int, y: int, new_type: str):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                try:
                    self.change_cell_type(i, j, new_type)
                except BadParameter:
                    continue

    def try_to_place_ship(self, x: int, y: int):
        cell = self._field[x][y]
        print(self._field_size)
        if (cell != self._cell_types['taken']) and not isinstance(cell, Ship):
            self.change_cell_type(x, y, 'ship')
            self.set_around(x, y, 'taken')
        else:
            raise InaccessiblePlace

    def change_cell_type(self, x: int, y: int, new_type: str):
        self._check(x, y)

        if new_type == 'ship':
            self._field[x][y] = Ship(x, y)
        else:
            self._field[x][y] = self._cell_types[new_type]

    def get_cell(self, x: int, y: int):
        self._check(x, y)

        return self._field[x][y]

    def random_arrangement_of_ships(self):
        ships_count = self._ships_count

        while ships_count:
            x = randint(0, self._field_size - 1)
            y = randint(0, self._field_size - 1)

            try:
                self.try_to_place_ship(x, y)
                ships_count -= 1
            except InaccessiblePlace:
                continue

    @staticmethod
    def _create_line(line: list):
        result = ''
        for cell in line:
            if isinstance(cell, Ship):
                result += str(cell) + ' '
            elif cell:
                print(cell, end=' ')
                result += str(cell) + ' '
            else:
                print(' ~ ', end=' ')
                result += ' ~  '

        return result

    @staticmethod
    def _create_hidden_line(line: list):
        result = ''
        for cell in line:
            if isinstance(cell, Ship):
                if cell.is_alive:
                    result += ' ~  '
                else:
                    print(cell, end=' ')
                    result += str(cell) + ' '
            elif cell:
                print(cell, end=' ')
                result += str(cell) + ' '
            else:
                print(' ~ ', end=' ')
                result += ' ~  '

        return result

    def __str__(self):
        result = '  '
        for i in range(self._field_size):
            result += f' {i}  '

        result += '\n'

        for i, line in enumerate(self._field):
            result += f"{i} " + self._create_line(line) + '\n'
            print()

        return result

    @classmethod
    def show_both_fields(cls, player: int, hide: bool = True):
        result = '  '
        for i in range(cls._field_size):
            result += f' {i}  '

        result += ' ' * 6 + result + '\n'

        for i in range(cls._field_size):
            if not hide:
                for field in cls._fields:
                    result += f'{i} ' + cls._create_line(field._field[i]) + ' ' * 6
                    print(' ' * 6)

                result += '\n'
                print('\n')

            if player == 1:
                result += f'{i} ' + cls._create_line(cls._fields[0]._field[i]) + ' ' * 6
                result += f'{i} ' + cls._create_hidden_line(cls._fields[1]._field[i]) + '\n'
            else:
                result += f'{i} ' + cls._create_hidden_line(cls._fields[0]._field[i]) + ' ' * 6
                result += f'{i} ' + cls._create_line(cls._fields[1]._field[i]) + '\n'

        return result + '\n'


class BadParameter(Exception):
    pass


class InaccessiblePlace(Exception):
    pass
