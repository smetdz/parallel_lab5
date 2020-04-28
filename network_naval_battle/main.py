from server import Server
from game import Game


if __name__ == '__main__':
    server = Server()

    game = Game(server)
    game.start_game()

    server.close_connection()
