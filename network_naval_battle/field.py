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

    def __init__(self):
        self._field = [[self._cell_types['water'] for _ in range(10)] for _ in range(10)]
        self._fields.append(self)

    @staticmethod
    def _check(x: int, y: int):
        if x not in range(0, 10) or y not in range(0, 10):
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
        if self._field[x][y] != self._cell_types['taken']:
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
        for i in range(10):
            result += f' {i}  '

        result += '\n'

        for i, line in enumerate(self._field):
            result += f"{i} " + self._create_line(line) + '\n'
            print()

        return result

    @classmethod
    def show_both_fields(cls, player: int):
        result = '  '
        for i in range(10):
            result += f' {i}  '

        result += ' ' * 6 + result + '\n'

        for i in range(10):
            # for field in cls._fields:
            #     result += f'{i} ' + cls._create_line(field._field[i]) + ' ' * 6
            #     print(' ' * 6)

            if player == 1:
                result += f'{i} ' + cls._create_line(cls._fields[0]._field[i]) + ' ' * 6
                result += f'{i} ' + cls._create_hidden_line(cls._fields[1]._field[i]) + '\n'
            else:
                result += f'{i} ' + cls._create_hidden_line(cls._fields[0]._field[i]) + ' ' * 6
                result += f'{i} ' + cls._create_line(cls._fields[1]._field[i]) + '\n'

        return result


class BadParameter(Exception):
    pass


class InaccessiblePlace(Exception):
    pass
