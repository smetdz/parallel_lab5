import socket


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', 5001))
        self.server_socket.listen(2)

    def get_clients(self):
        return [self.server_socket.accept() for _ in range(2)]

    @staticmethod
    def close_connection(clients: list):
        for client in clients:
            client.close()

    def send(self):
        pass

    def read(self):
        pass
