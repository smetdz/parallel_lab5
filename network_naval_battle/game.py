from player import Player
from field import Field, BadParameter, InaccessiblePlace, Ship
from server import Server
from threading import Thread


class Game:
    def __init__(self, server: Server):
        self._server = server

    def start_game(self):
        field1 = Field()
        field2 = Field()

        client1, client2 = self._server.get_clients()
        print(client1, client2)

        player1 = Player(client1[0], client1[1], field1, 'player1')
        player2 = Player(client2[0], client2[1], field2, 'player2')

        self._game_process(player1, player2)

    def _tell_to_player(self, player: Player, message: str, need_answer: bool = False):
        if need_answer:
            self._server.send(player.socket, message)
            return self._server.read(player.socket).strip()
        else:
            self._server.send(player.socket, message, False)

    def _move(self, player1: Player, player2: Player):
        while True:
            self._show_fields(player1, player2)
            message = f"The {player1.name} walks"

            self._tell_to_player(player2, message)
            answer = self._tell_to_player(player1, message, True)

            x, y = answer.split()
            x, y = int(x), int(y)

            try:
                cell = player2.field.get_cell(x, y)
            except BadParameter:
                message = "Wrong place. Try again"
                self._tell_to_player(player1, message)
                continue

            if isinstance(cell, Ship):
                if cell.is_alive:
                    cell.kill()
                    player2.ships_count -= 1
                    player2.field.set_around(x, y, 'fired')

                    if player2.ships_count:
                        continue

                    break
                else:
                    message = "Wrong place. Try again"
                    self._tell_to_player(player1, message)
                    continue
            elif cell == ' * ':
                message = "Wrong place. Try again"
                self._tell_to_player(player1, message)
                continue

            player2.field.change_cell_type(x, y, 'fired')

            break

    def _show_fields(self, player1: Player, player2: Player):
        message1 = Field.show_both_fields(1)
        message2 = Field.show_both_fields(2)

        self._tell_to_player(player1, message1)
        self._tell_to_player(player2, message2)

    def _game_process(self, player1: Player, player2: Player):
        cl_thd1 = Thread(target=self._ships_arrangement, args=(player1, ))
        cl_thd2 = Thread(target=self._ships_arrangement, args=(player2, ))

        cl_thd1.start()
        cl_thd2.start()

        cl_thd1.join()
        cl_thd2.join()

        while True:
            self._move(player1, player2)

            if self._loose_check(player2):
                winner = player1
                break

            self._move(player2, player1)

            if self._loose_check(player1):
                winner = player2
                break

        message = f"Player {winner.name} won!"

        self._tell_to_player(player1, message)
        self._tell_to_player(player2, message)

    @staticmethod
    def _loose_check(player: Player):
        if player.is_lose:
            return True

    def _ships_arrangement(self, player: Player):
        message = '1 - Random ships position, 2 - Arrange ships yourself'

        answer = self._tell_to_player(player, message, True)

        if int(answer) - 1:
            count = player.field.ships_count
            print(type(count))
            while count:
                message = str(player.field) + "\n Select the cell where you want to put the ship\n" \
                                              "The answer should be this kind: x y"

                answer = self._tell_to_player(player, message, True)
                x, y = answer.split()

                try:
                    player.field.try_to_place_ship(int(x), int(y))
                    count -= 1
                except InaccessiblePlace:
                    message = 'Сan`t be put here. Try again'
                    self._tell_to_player(player, message)
                    continue
        else:
            player.field.random_arrangement_of_ships()
            message = str(player.field)

            self._tell_to_player(player, message)
